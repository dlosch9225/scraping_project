# update_hdf5.py
import pandas as pd
import os
from pathlib import Path

CSV_PATH = Path("../data/usgs.csv")
HDF5_PATH = Path("../data/dataset.h5")

df = pd.read_csv(CSV_PATH)
df["date"] = pd.to_datetime(df["date"])

with pd.HDFStore(HDF5_PATH, mode="a") as store:
    if "earthquakes" in store:
        existing = store["earthquakes"]
        combined = pd.concat([existing, df], ignore_index=True)
        combined = combined.drop_duplicates(subset=["date", "place"], keep="last")
        store.put("earthquakes", combined, format="table")
    else:
        store.put("earthquakes", df, format="table")

print("✅ HDF5 file updated with CSV content.")