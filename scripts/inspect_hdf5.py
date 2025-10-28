import pandas as pd
import os

HDF5_FILE = os.path.join("../data", "dataset.h5")

# Verifica que el archivo existe
if not os.path.exists(HDF5_FILE):
    print("❌ El archivo HDF5 no existe.")
else:
    with pd.HDFStore(HDF5_FILE) as store:
        print("📁 Contenido del archivo HDF5:")
        print(store)
        print("\n🔑 Claves (keys) disponibles:")
        print(store.keys())

        # Leer y mostrar los primeros registros de cada tabla
        for key in store.keys():
            print(f"\n🧾 Datos de {key}:")
            df = store.select(key)
            print(df.head())
