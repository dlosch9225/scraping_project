import pandas as pd
import os
import tables
import logging

# Disable BLOSC2 compression to avoid compatibility issues
tables.parameters.BLOSC2_ENABLED = False

# Absolute path to the HDF5 file
HDF5_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "dataset.h5"))

def save_to_hdf(new_data: pd.DataFrame, key: str):
    """
    Save a new DataFrame to the HDF5 file, merging with existing data under the same key.
    Duplicates are removed based on the 'date' column.
    """
    try:
        # 🧪 Print diagnostic information before saving
        print(f"\n📊 [DEBUG] Saving data for key: '{key}'")
        print(f"➡️ Columns: {new_data.columns.tolist()}")
        print(f"➡️ First rows:\n{new_data.head()}\n")

        print(f"📝 Attempting to save {len(new_data)} rows under key '{key}'")

        # Absolute path to the HDF5 file
        hdf5_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "dataset.h5"))
        if os.path.exists(hdf5_path):
            with pd.HDFStore(hdf5_path, mode='r') as store:
                existing_data = store[key] if key in store else pd.DataFrame()
                print(f"📁 Existing records for key '{key}': {len(existing_data)} rows")
        else:
            existing_data = pd.DataFrame()
            print("📁 HDF5 file does not exist. A new one will be created.")

        # Merge new data with existing data
        combined = pd.concat([existing_data, new_data], ignore_index=True)

        # Ensure 'date' column is datetime for proper deduplication and sorting
        if "date" in combined.columns:
            combined["date"] = pd.to_datetime(combined["date"], errors="coerce")
        else:
            print("⚠️ WARNING: 'date' column not found in the DataFrame!")

        # Drop duplicates based on 'date' and sort by date
        combined = combined.drop_duplicates(subset="date", keep="last")
        combined = combined.sort_values("date", na_position="last")

        # Write combined data back to HDF5
        with pd.HDFStore(hdf5_path, mode='a') as store:
            store.put(key, combined, format="table")

        print(f"✅ Successfully saved: key '{key}' now has {len(combined)} rows.\n")

    except Exception as e:
        print(f"❌ ERROR saving to HDF5 under key '{key}': {e}")
        logging.error(f"Error saving to HDF5: {e}")
        raise



# Optional test
if __name__ == "__main__":
    df_test = pd.DataFrame([{
        "date": "2025-10-20",
        "value": 99999,
        "source": "Test Source"
    }])
    save_to_hdf(df_test, "bitcoin")
    print("✅ Test saved to HDF5.")

