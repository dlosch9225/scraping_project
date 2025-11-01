import os
import shutil
from datetime import datetime

# Resolve project root path based on this script's location
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Define source and destination paths
source = os.path.join(BASE_DIR, "data", "dataset.h5")
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_dir = os.path.join(BASE_DIR, "backups")
backup_path = os.path.join(backup_dir, f"dataset_backup_{timestamp}.h5")

# Ensure backup directory exists
os.makedirs(backup_dir, exist_ok=True)

# Copy file
if os.path.exists(source):
    shutil.copy2(source, backup_path)
    print(f"✅ Backup created at: {backup_path}")
else:
    print(f"❌ Backup failed — source file not found at: {source}")
