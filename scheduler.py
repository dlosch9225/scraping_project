"""
Daily Scraper Scheduler

This script runs all scraping functions (Bitcoin, Weather, Earthquakes)
at 11:00 AM daily, but only during a predefined 9-day window.

It uses a state file (scheduler_state.txt) to determine the window start.
"""

import schedule
import time
import os
import logging
from datetime import datetime, timedelta

# -------------------- PATH SETUP --------------------

# Get absolute path to project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

STATE_FILE = os.path.join(LOG_DIR, "scheduler_state.txt")
LOG_FILE = os.path.join(LOG_DIR, "scheduler.log")

# -------------------- LOGGING SETUP --------------------

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------- IMPORT SCRAPERS --------------------

from scrapers.scraper import (
    scrape_coingecko_bitcoin,
    save_bitcoin_data,
    scrape_open_meteo,
    save_open_meteo_data,
    scrape_usgs,
    save_usgs_data
)

# -------------------- JOB DEFINITION --------------------
def job():
    """
    Executes all scraper functions daily.
    """
    print("⏰ Running scheduled scrapers...")
    logging.info("Started job...")

    # --- Bitcoin ---
    print("💰 Scraping Bitcoin...")
    df_btc = scrape_coingecko_bitcoin()
    if not df_btc.empty:
        save_bitcoin_data(df_btc)
        logging.info("✅ Bitcoin data saved.")
    else:
        print("⚠️ No Bitcoin data retrieved.")
        logging.warning("❌ Bitcoin data unavailable.")

    # --- Weather ---
    print("🌤️ Scraping weather data...")
    df_weather = scrape_open_meteo()
    if not df_weather.empty:
        save_open_meteo_data(df_weather)
        logging.info("✅ Weather data saved.")
    else:
        print("⚠️ No weather data retrieved.")
        logging.warning("❌ Weather data unavailable.")

    # --- Earthquakes ---
    print("🌍 Scraping earthquake data...")
    df_quakes = scrape_usgs()
    if not df_quakes.empty:
        save_usgs_data(df_quakes)
        logging.info("✅ Earthquake data saved.")
    else:
        print("⚠️ No earthquake data retrieved.")
        logging.warning("❌ Earthquake data unavailable.")

    print("✅ All scrapers completed.\n")
    logging.info("All scrapers completed.\n")


# -------------------- SCHEDULER SETUP --------------------

schedule.every().day.at("11:00").do(job)

print("📅 Scheduler started. Waiting for the next job...")
logging.info("Scheduler initialized.")

# Keep running
while True:
    schedule.run_pending()
    time.sleep(60)
