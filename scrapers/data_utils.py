from pathlib import Path
import pandas as pd

def load_data(csv_filename: str, hdf5_key: str) -> pd.DataFrame:
    """
    Load data from a CSV file. If the file doesn't exist, load from HDF5 using a given key.

    Args:
        csv_filename (str): Filename to look for in /data.
        hdf5_key (str): Key to use when reading from dataset.h5 if CSV is missing.

    Returns:
        pd.DataFrame: Loaded data (empty if nothing found).
    """
    # Base paths
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    csv_path = data_dir / csv_filename
    hdf5_path = data_dir / "dataset.h5"

    # Try CSV first
    if csv_path.exists():
        print(f"✅ Data loaded from CSV: {csv_filename}")
        try:
            return pd.read_csv(csv_path)
        except Exception as e:
            print(f"⚠️ Error reading CSV: {e}")
            return pd.DataFrame()

    # Try HDF5
    if not hdf5_path.exists():
        print("⚠️ HDF5 file not found.")
        return pd.DataFrame()

    try:
        with pd.HDFStore(hdf5_path, mode="r") as store:
            if hdf5_key not in store:
                print(f"⚠️ Key '{hdf5_key}' not found in HDF5.")
                return pd.DataFrame()
            print(f"✅ Data loaded from HDF5 key: {hdf5_key}")
            return store[hdf5_key]
    except Exception as e:
        print(f"⚠️ Error reading from HDF5: {e}")
        return pd.DataFrame()
