"""
Scraper Script for Multiple Data Sources

This script loads website metadata, scrapes current data
(Bitcoin price from CoinGecko, weather from Meteostat, and earthquakes from USGS),
and saves it into CSV files, ensuring there are no duplicate entries for the same date.
Includes logging and retry logic for robustness.
"""

import os
import time
import logging
import requests
import pandas as pd
from datetime import datetime, timezone
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from storage import save_to_hdf



# ---------- CONFIGURATION ----------
DATA_DIR = "../data"
BITCOIN_CSV = os.path.join(DATA_DIR, "bitcoin.csv")
METEOSTAT_CSV = os.path.join(DATA_DIR, "meteostat.csv")
USGS_CSV = os.path.join(DATA_DIR, "usgs.csv")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="../logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------- HELPER FUNCTIONS ----------

def get_with_retry(url, headers=None, params=None, retries=3, backoff_factor=0.5, timeout=10):
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("https://", adapter)

    try:
        response = session.get(url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
        return response
    except Exception as e:
        logging.error(f"Request failed after retries: {e}")
        return None

# ---------- SCRAPER FUNCTIONS ----------

def load_websites_csv() -> pd.DataFrame:
    """
    Load metadata about websites from the root-level websites.csv file.
    """
    try:
        # ✅ Build absolute path to websites.csv (one level up from this script)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, "websites.csv")

        # Check existence
        if not os.path.exists(csv_path):
            logging.error(f"websites.csv not found at {csv_path}")
            print(f"Could not find websites.csv at: {csv_path}")
            return pd.DataFrame()

        # Load CSV
        df = pd.read_csv(csv_path)
        logging.info(f"Website metadata loaded successfully from {csv_path}")
        return df

    except Exception as e:
        logging.error(f"Failed to load websites.csv: {e}")
        print("Could not load websites.csv.")
        return pd.DataFrame()


def scrape_coingecko_bitcoin() -> pd.DataFrame:
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = get_with_retry(url)
    if response is None:
        return pd.DataFrame()

    try:
        data = response.json()
        price = data["bitcoin"]["usd"]
        today = datetime.now().strftime("%Y-%m-%d")

        df = pd.DataFrame([{
            "date": today,
            "value": price,
            "source": "CoinGecko - Bitcoin"
        }])
        logging.info(f"Bitcoin price (API) retrieved successfully: ${price}")
        return df
    except Exception as e:
        logging.error(f"Error parsing API response: {e}")
        return pd.DataFrame()

def save_bitcoin_data(df: pd.DataFrame):
    if df.empty:
        logging.warning("No Bitcoin data to save.")
        return

    if os.path.exists(BITCOIN_CSV):
        existing = pd.read_csv(BITCOIN_CSV)
        if not df.empty and "date" in df.columns and df.iloc[0]["date"] in existing["date"].values:
            logging.info("Bitcoin data for today's date already exists. Skipping save.")
            return

    df.to_csv(BITCOIN_CSV, mode="a", header=not os.path.exists(BITCOIN_CSV), index=False)
    logging.info(f"Bitcoin data saved to {BITCOIN_CSV}")


def scrape_open_meteo(latitude: float = 52.52, longitude: float = 13.405) -> pd.DataFrame:
    """
    Fetch current weather data for a given location using the Open-Meteo API.

    Args:
        latitude (float): Latitude of the location (default: Berlin).
        longitude (float): Longitude of the location (default: Berlin).

    Returns:
        pd.DataFrame: Weather data with columns date, temperature, wind_speed, weather_code, and source.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "current_weather" not in data:
            logging.warning("No current weather data found in Open-Meteo response.")
            return pd.DataFrame()

        weather = data["current_weather"]
        df = pd.DataFrame([{
            "date": datetime.now().strftime("%Y-%m-%d"),
            "temperature": weather.get("temperature"),
            "wind_speed": weather.get("windspeed"),
            "weather_code": weather.get("weathercode"),
            "source": "Open-Meteo API"
        }])

        logging.info(f"Open-Meteo weather data retrieved: {df.to_dict(orient='records')[0]}")
        return df

    except Exception as e:
        logging.error(f"Error fetching Open-Meteo weather data: {e}")
        return pd.DataFrame()


def save_open_meteo_data(df: pd.DataFrame):
    """
    Save Open-Meteo weather data to CSV and HDF5, avoiding duplicates in CSV.
    """
    filename = "../data/open_meteo.csv"

    if df.empty:
        logging.warning("No Open-Meteo data to save.")
        return

    # Check if already exist in CSV
    already_exists = False
    if os.path.exists(filename):
        existing = pd.read_csv(filename)
        if not df.empty and "date" in df.columns and df.iloc[0]["date"] in existing["date"].values:
            logging.info("Open-Meteo data for today's date already exists. Skipping CSV save.")
            already_exists = True

    # Keep in CSV just if is a new register
    if not already_exists:
        df.to_csv(filename, mode="a", header=not os.path.exists(filename), index=False)
        logging.info(f"Open-Meteo data saved to {filename}")

    # 👉 Keep always in HDF5
    try:
        save_to_hdf(df, "weather")
        logging.info("Open-Meteo data also saved to dataset.h5 (HDF5).")
    except Exception as e:
        logging.error(f"Error saving weather data to HDF5: {e}")



def scrape_usgs() -> pd.DataFrame:
    """
    Scrape recent earthquake data from the USGS API.
    Filters for magnitude >= 2.5 and returns relevant info.
    """
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    response = get_with_retry(url)
    if response is None:
        logging.error("Failed to fetch data from USGS.")
        return pd.DataFrame()

    try:
        data = response.json()
        records = []

        for feature in data["features"]:
            props = feature["properties"]
            mag = props.get("mag")
            place = props.get("place")
            timestamp = props.get("time")

            # Only include earthquakes with magnitude >= 2.5
            if mag is None or mag < 2.5:
                continue

            # ✅ Updated timestamp handling (timezone-aware)
            date_str = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime("%Y-%m-%d")

            records.append({
                "date": date_str,
                "value": mag,
                "place": place,
                "source": "USGS Earthquake Feed"
            })

        if not records:
            logging.info("No significant earthquakes found today.")
            return pd.DataFrame()

        df = pd.DataFrame(records)
        logging.info(f"{len(df)} earthquake(s) parsed from USGS.")
        return df

    except Exception as e:
        logging.error(f"Error parsing USGS data: {e}")
        return pd.DataFrame()


def save_usgs_data(df: pd.DataFrame):
    if df.empty:
        logging.warning("No USGS data to save.")
        return

    if os.path.exists(USGS_CSV):
        existing = pd.read_csv(USGS_CSV)
        df = df[~df.apply(lambda row: ((existing["date"] == row["date"]) & (existing["place"] == row["place"])).any(), axis=1)]

        if df.empty:
            logging.info("All USGS records already exist. Skipping save.")
            return

    df.to_csv(USGS_CSV, mode="a", header=not os.path.exists(USGS_CSV), index=False)
    logging.info(f"USGS data saved to {USGS_CSV}")

    # Keep also in HDF5
    try:
        save_to_hdf(df, "earthquakes")
        logging.info("USGS data also saved to dataset.h5 (HDF5).")
    except Exception as e:
        logging.error(f"Error saving earthquake data to HDF5: {e}")


# ---------- MAIN EXECUTION ----------

def main():
    try:
        websites = load_websites_csv()
        print("Websites loaded successfully:\n")
        print(websites[["Website Name", "URL"]])
    except Exception:
        print("Could not load websites.csv.")
        return

    # CoinGecko
    df_btc = scrape_coingecko_bitcoin()
    if not df_btc.empty:
        print(f"\nBitcoin price scraped: ${df_btc.iloc[0]['value']:,.2f}")
    else:
        print("\nBitcoin price not available.")
    save_bitcoin_data(df_btc)
    time.sleep(1)

    # Open-Meteo
    print("\nWeather data from Open-Meteo:")
    df_weather = scrape_open_meteo()
    if not df_weather.empty:
        print(df_weather.to_string(index=False))
    else:
        print("No weather data available.")
    save_open_meteo_data(df_weather)

    # USGS
    print("\nEarthquake data from USGS:")
    df_usgs = scrape_usgs()
    if not df_usgs.empty:
        print(df_usgs.head().to_string(index=False))
    else:
        print("No significant earthquake data found.")
    save_usgs_data(df_usgs)

if __name__ == "__main__":
    main()
