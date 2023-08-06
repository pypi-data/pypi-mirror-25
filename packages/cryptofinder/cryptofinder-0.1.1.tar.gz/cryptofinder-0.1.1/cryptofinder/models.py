from .config import DBFILE
from .utilities import validate_json_entry_types
from peewee import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from ww import f as fstr
import datetime
import json
import os
import requests
import time

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
db = SqliteDatabase(DBFILE)

class Base(Model):
  class Meta:
    database = db

  def __str__(self):
    attrs = {}
    for k in self._data.keys():
      try:
        attrs[k] = str(getattr(self, k))
      except:
        attrs[k] = json.dumps(getattr(self, k))
    return str(attrs)

  @property
  def props(self):
    props = {}
    for k in self._data.keys():
      try:
        props[k] = str(getattr(self, k))
      except:
        props[k] = json.dumps(getattr(self, k))
    return props

class Coin(Base):
  symbol = TextField(default="")
  name = TextField(default='')
  # avail_supply_ratio
  total_supply = FloatField(default=0.0)
  avail_supply = FloatField(default=0.0)
  avail_supply_ratio = FloatField(default=0.0)
  # daily_volume_ratio
  daily_volume_usd = FloatField(default=0.0)
  market_cap_usd = FloatField(default=0.0)
  daily_volume_ratio = FloatField(default=0.0)
  # prices
  price_btc = FloatField(default=0.0)
  price_usd = FloatField(default=0.0)
  percent_change_1h = FloatField(default=0.0)
  percent_change_24h = FloatField(default=0.0)
  percent_change_7d = FloatField(default=0.0)
  rank = IntegerField(default=0)
  last_updated = DateTimeField(default=datetime.datetime.now)

  @classmethod
  def types(self):
    return {
      'floats': [
        '24h_volume_usd',
        'available_supply',
        'market_cap_usd',
        'percent_change_1h',
        'percent_change_24h',
        'percent_change_7d',
        'price_btc',
        'price_usd',
        'total_supply',
      ],
      'ints': [
        'rank',
        'last_updated'
      ],
      'strs': [
        'name',
        'symbol'
      ]
    }

class Ticker(Base):
  parsed_at = DateTimeField(default=datetime.datetime.now)
  results = IntegerField(default=0)

  @classmethod
  def latest(self):
    try:
      return Ticker.select().order_by(Ticker.id.desc()).get()
    except:
      return

  @classmethod
  def stale(self):
    latest = Ticker.latest()
    if not latest:
      return True
    if datetime.datetime.now() > ( latest.parsed_at + datetime.timedelta(minutes = 10) ):
      return True

  @classmethod
  def refresh(self):
    try:
      entries = list( requests.get('https://api.coinmarketcap.com/v1/ticker/').json() )
    except ConnectionError:
      return

    for entry in entries:
      entry = Ticker.clean_entry(entry)
      symbol = entry.get('symbol')

      # Delete old coin instance
      try:
        coin = Coin.get(symbol=symbol)
        logger.debug( fstr("Deleting stale data for {coin.symbol}") )
        coin.delete_instance()
      except:
        pass

      # Create new coin instance
      coin = Coin.create(**entry)
      logger.debug( fstr("Cached data for {coin.symbol}") )

    ticker = Ticker.create(results=len(entries))
    return ticker

  @classmethod
  def clean_entry(self, entry):
    coin_types = Coin.types()
    entry = validate_json_entry_types(coin_types, entry)

    entry.pop('id')
    entry['daily_volume_usd'] = entry.pop('24h_volume_usd')
    entry['avail_supply'] = entry.pop('available_supply')
    entry['last_updated'] = datetime.datetime.utcfromtimestamp( entry.pop('last_updated') )

    try:
      entry['daily_volume_ratio'] = entry['daily_volume_usd'] / entry['market_cap_usd']
    except ZeroDivisionError:
      entry['daily_volume_ratio'] = 0.0

    try:
      entry['avail_supply_ratio'] = entry['avail_supply'] / entry['total_supply']
    except ZeroDivisionError:
      entry['avail_supply_ratio'] = 0.0

    return entry

class Database:
  @classmethod
  def connect(self):
    drop = ui.get('drop')
    if drop:
      os.remove(DBFILE)
      open(DBFILE, 'w+')

    tables = [Coin, Ticker]
    db.connect()
    db.create_tables(tables, safe=True)

  @classmethod
  def disconnect(self):
    db.close()