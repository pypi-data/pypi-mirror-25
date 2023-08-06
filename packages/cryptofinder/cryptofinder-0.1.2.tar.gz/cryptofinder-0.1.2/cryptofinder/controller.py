from .models import Coin, Database, Ticker
from .views import CoinView
from ww import f as fstr
import os

class Controller:
  @classmethod
  def main(self):
    Database.connect()

    # Set local variables for user input
    avail_supply = ui.get('avail_supply')
    avail_supply_ratio = ui.get('avail_supply_ratio')
    daily_volume = ui.get('daily_volume')
    daily_volume_ratio = ui.get('daily_volume_ratio')
    json = ui.get('json')
    market_cap = ui.get('market_cap')
    offline = ui.get('offline')
    quiet = ui.get('quiet')

    # Grab or update ticker
    ticker = Ticker.latest()
    if not ticker or ticker.stale:
      if not offline:
        ticker = Ticker.refresh()
      else:
        logger.error("Nothing to parse.")
        return
    else:
      logger.info("CoinMarketCap ticker is up to date.")

    # Grab coins
    coins = Coin.select().where(
      Coin.avail_supply <= avail_supply[1],
      Coin.avail_supply >= avail_supply[0], 
      Coin.avail_supply_ratio >= avail_supply_ratio,
      Coin.daily_volume_ratio >= daily_volume_ratio, 
      Coin.daily_volume_usd <= daily_volume[1],
      Coin.daily_volume_usd >= daily_volume[0],
      Coin.market_cap_usd <= market_cap[1],
      Coin.market_cap_usd >= market_cap[0], 
    )
    
    # Output results
    view = CoinView(coins)
    if not quiet:
      view.table()
      ticker_date = ticker.parsed_at.strftime("%Y-%m-%d")
      ticker_time = ticker.parsed_at.strftime("%I:%M:%S %p")
      logger.info( fstr("Data cached {ticker_date} @ {ticker_time}.") )
    if json:
      view.json()

    Database.disconnect()

    return True