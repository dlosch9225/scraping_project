from pathlib import Path
import pandas as pd
import os  # ✅ NECESARIO para rutas
import tables
import logging  # ✅ NECESARIO para logging


# Desactivar BLOSC2 si da problemas
tables.parameters.BLOSC2_ENABLED = False

HDF5_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "dataset.h5"))



def save_to_hdf(new_data: pd.DataFrame, key: str):
    """
    Save a new DataFrame to HDF5 file, combining with existing data under the same key.
    Avoids duplicates by 'date'.
    """
    try:
        # Load existing data (if file exists and key exists)
        if os.path.exists(HDF5_FILE):
            with pd.HDFStore(HDF5_FILE, mode='r') as store:
                existing_data = store[key] if key in store else pd.DataFrame()
        else:
            existing_data = pd.DataFrame()

        # Combine both datasets
        combined = pd.concat([existing_data, new_data], ignore_index=True)

        # ✅ Ensure consistent datetime type for sorting and deduplication
        if "date" in combined.columns:
            combined["date"] = pd.to_datetime(combined["date"], errors="coerce")

        combined = combined.drop_duplicates(subset="date", keep="last")
        combined = combined.sort_values("date", na_position="last")

        # Save combined data back to HDF5
        with pd.HDFStore(HDF5_FILE, mode='w') as store:
            store.put(key, combined, format="table")

        logging.info(f"✅ Data saved to {HDF5_FILE} under key '{key}' with {len(combined)} total records.")

    except Exception as e:
        logging.error(f"❌ Error saving data to HDF5: {e}")
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

