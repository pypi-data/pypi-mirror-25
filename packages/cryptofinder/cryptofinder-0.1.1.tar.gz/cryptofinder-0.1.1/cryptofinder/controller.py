from .models import Coin, Database, Ticker
from .views import CoinView
from ww import f as fstr
import os
import time

class Controller():
  def __init__(self):
    pass

  @classmethod
  def main(self):
    Database.connect()

    # Set local variables for user input
    offline = ui.get('offline')
    avail_supply = ui.get('avail_supply')
    avail_supply_ratio = ui.get('avail_supply_ratio')
    daily_volume = ui.get('daily_volume')
    daily_volume_ratio = ui.get('daily_volume_ratio')
    market_cap = ui.get('market_cap')
    json = ui.get('json')
    quiet = ui.get('quiet')

    avail_supply_min = avail_supply[0]
    avail_supply_max = avail_supply[1]
    market_cap_min = market_cap[0]
    market_cap_max = market_cap[1]
    daily_volume_min = daily_volume[0]
    daily_volume_max = daily_volume[1]

    # Display arguments to user
    logger.info('Query parameters:')
    logger.info( fstr("Available supply max: {avail_supply_max}") )
    logger.info( fstr("Available supply min: {avail_supply_min}") )
    logger.info( fstr("Available supply ratio: {avail_supply_ratio}") )
    logger.info( fstr("Daily volume max: {daily_volume_max}") )
    logger.info( fstr("Daily volume min: {daily_volume_min}") )
    logger.info( fstr("Daily volume ratio: {daily_volume_ratio}") )
    logger.info( fstr("Market cap max: {market_cap_max}") )
    logger.info( fstr("Market cap min: {market_cap_min}") )
    logger.info('')
    if offline:
      logger.info("Offline mode enabled.")
    
    # Check for existing ticker instance
    ticker = Ticker.latest()
    if ticker:
      logger.debug("Ticker has been cached.")
    else:
      logger.debug("Ticker cache does not exist.")
      if offline:
        logger.info("Offline mode enabled.")
        logger.error("Nothing to parse.")
        return

    # Refresh ticker if it is stale
    if Ticker.stale() and not offline:
      logger.warning("Ticker is not up to date.")
      logger.info("Updating entries.")

      ticker = Ticker.refresh()
      if not ticker:
        logger.error("Connection failed.")
        return

    # Grab Coin instances matching user request
    coins = Coin.select().where(
      Coin.avail_supply <= avail_supply_max,
      Coin.avail_supply >= avail_supply_min, 
      Coin.avail_supply_ratio >= avail_supply_ratio,
      Coin.daily_volume_ratio >= daily_volume_ratio, 
      Coin.daily_volume_usd <= daily_volume_max,
      Coin.daily_volume_usd >= daily_volume_min,
      Coin.market_cap_usd <= market_cap_max,
      Coin.market_cap_usd >= market_cap_min, 
    )
    
    # Output results
    view = CoinView(coins)

    if not quiet:
      matches = len(coins)
      logger.info( fstr("{matches}/{ticker.results} coins match your query.") )
      
      view.table()

      ticker_date = ticker.parsed_at.strftime("%Y-%m-%d")
      ticker_time = ticker.parsed_at.strftime("%I:%M:%S %p")
      logger.info( fstr("Data retrieved {ticker_date} @ {ticker_time}") )

    if json:
      view.json()

    Database.disconnect()

    return True