import os
import requests
import pandas as pd
from datetime import datetime
from storage import save_to_hdf

# Config paths
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
BITCOIN_CSV = os.path.join(DATA_DIR, "bitcoin.csv")
OPEN_METEO_CSV = os.path.join(DATA_DIR, "open_meteo.csv")
USGS_CSV = os.path.join(DATA_DIR, "usgs.csv")

MISSING_DATES = ["2025-10-29", "2025-10-30"]


# ----------------------------------
# 1. CoinGecko Historical Scraper
# ----------------------------------

def get_bitcoin_price_for_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    url_date = date_obj.strftime("%d-%m-%Y")
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/history?date={url_date}"

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        price = data["market_data"]["current_price"]["usd"]
        return pd.DataFrame([{
            "date": date_str,
            "value": price,
            "source": "CoinGecko - Bitcoin"
        }])
    except Exception as e:
        print(f"❌ Failed to retrieve BTC data for {date_str}: {e}")
        return pd.DataFrame()


# ----------------------------------
# 2. Open-Meteo Historical Scraper
# ----------------------------------

def get_open_meteo_for_date(date_str, lat=52.52, lon=13.405):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": date_str,
        "end_date": date_str,
        "hourly": "temperature_2m,windspeed_10m,weathercode",
        "timezone": "Europe/Berlin"
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        hourly = pd.DataFrame(data["hourly"])
        # Use noon (12:00) data if available
        idx = hourly["time"].apply(lambda x: "12:00" in x)
        row = hourly[idx].iloc[0]
        df = pd.DataFrame([{
            "date": date_str,
            "temperature": row["temperature_2m"],
            "wind_speed": row["windspeed_10m"],
            "weather_code": row["weathercode"],
            "source": "Open-Meteo API"
        }])
        return df
    except Exception as e:
        print(f"❌ Failed to retrieve weather data for {date_str}: {e}")
        return pd.DataFrame()


# ----------------------------------
# 3. USGS Earthquake Historical Scraper
# ----------------------------------

def get_usgs_for_date(date_str):
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": date_str,
        "endtime": date_str,
        "minmagnitude": 2.5
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        records = []
        for feature in data["features"]:
            props = feature["properties"]
            mag = props.get("mag")
            place = props.get("place")
            timestamp = props.get("time")
            date_clean = datetime.utcfromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")

            records.append({
                "date": date_clean,
                "value": mag,
                "place": place,
                "source": "USGS Earthquake Feed"
            })
        return pd.DataFrame(records)
    except Exception as e:
        print(f"❌ Failed to retrieve USGS data for {date_str}: {e}")
        return pd.DataFrame()


# ----------------------------------
# 🔁 Main recovery loop
# ----------------------------------

for missing_date in MISSING_DATES:
    print(f"\n📅 Recovering data for: {missing_date}")

    # Bitcoin
    btc_df = get_bitcoin_price_for_date(missing_date)
    if not btc_df.empty:
        btc_df.to_csv(BITCOIN_CSV, mode="a", header=not os.path.exists(BITCOIN_CSV), index=False)
        save_to_hdf(btc_df, "bitcoin")
        print("✅ Bitcoin data saved.")

    # Weather
    weather_df = get_open_meteo_for_date(missing_date)
    if not weather_df.empty:
        weather_df.to_csv(OPEN_METEO_CSV, mode="a", header=not os.path.exists(OPEN_METEO_CSV), index=False)
        save_to_hdf(weather_df, "weather")
        print("✅ Weather data saved.")

    # Earthquakes
    usgs_df = get_usgs_for_date(missing_date)
    if not usgs_df.empty:
        usgs_df.to_csv(USGS_CSV, mode="a", header=not os.path.exists(USGS_CSV), index=False)
        save_to_hdf(usgs_df, "earthquakes")
        print("✅ Earthquake data saved.")

print("\n🎉 Done recovering all missing data.")
