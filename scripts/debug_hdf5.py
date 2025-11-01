import pandas as pd

# Path to your HDF5 file
file_path = "../data/dataset.h5"

with pd.HDFStore(file_path, mode='r') as store:
    print("\n🔍 HDF5 Keys:")
    print(store.keys())
    print()

    for key in store.keys():
        print(f"📄 Preview of '{key}':")
        print(store[key].head(), "\n")
