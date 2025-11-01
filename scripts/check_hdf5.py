import os
import pandas as pd
from pandas.io.pytables import HDFStore

# Absolute path to dataset
hdf5_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "dataset.h5"))

print("📁 HDF5 File Content:")
store = HDFStore(hdf5_path)

print(f"<{type(store)}>")
print(f"File path: {hdf5_path}\n")

# List all keys
keys = store.keys()
print("🔑 Available HDF5 keys:")
print(keys, "\n")

# Show preview for each key
for key in keys:
    df = store[key]
    print(f"🔑 {key} — total rows: {len(df)}")
    print(df.head(5).to_string(index=False))
    print("-" * 50)

store.close()
