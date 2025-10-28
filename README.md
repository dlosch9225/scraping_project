# 🌐 Multi-Source Data Scraper

This Python project automatically scrapes and stores daily data from multiple public sources:
- 💰 **Bitcoin price** from CoinGecko  
- 🌤️ **Weather data** from Open-Meteo  
- 🌍 **Earthquake alerts** from USGS

Data is saved in both **CSV** and **HDF5** formats. A scheduler runs the scraper daily during a 9-day window. Logs and visualizations are included.

---

## 📚 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Automation](#automation)
- [Data Storage Format](#data-storage-format)
- [Data Structure](#data-structure)
- [Visualization](#visualization)
- [Testing & Validation](#testing--validation)
- [Known Limitations](#known-limitations)
- [Requirements](#requirements)
- [License](#license)

---

## ✨ Features

- ⏱️ **Automated daily scraping** at 11:00 AM (via `cron`)
- 💾 **Dual storage**: CSV + HDF5 with deduplication
- 📊 **Clean and styled visualizations** with Matplotlib
- 🧠 **Retry logic** and **error handling** for API calls
- 🧪 Modular, testable, and easy to expand

---

## 🏗️ Project Structure

```
scraping_project/
├── data/                    # CSVs and HDF5 data storage
├── logs/                    # All logs + scheduler state
├── scrapers/               # Core scraping logic
│   ├── scraper.py
│   ├── data_utils.py
├── plotting/               # All plots and visualizations
│   ├── plot_bitcoin.py
│   ├── open_meteo.py
│   ├── plot_usgs.py
├── scripts/                # Utility/debugging scripts
│   ├── force_update_hdf5.py
│   ├── inspect_hdf5.py
├── scheduler.py            # Daily job manager
├── start_scheduler.sh      # Script launched by cron
├── storage.py              # HDF5 logic
├── requirements.txt
└── websites.csv            # Metadata of scraped sources
```

## ⚙️ Installation

#### 1.  the repo:
```
git clone https://github.com/your_username/scraping_project.git
cd scraping_project
```

#### 2. Create a virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Install dependencies:
```
pip install -r requirements.txt
```
## 🚀 Usage

Run the scraper manually:
```
python scrapers/scraper.py
```

Or run the visualization:
```
python plotting/plot_bitcoin.py
```
## ⏰ Automation

The project uses cron to:

* Start the scheduler at system reboot
* Trigger scrapers daily at 11:00 AM

#### Cron Configuration Example (macOS/Linux)
```
@reboot /absolute/path/to/start_scheduler.sh
0 11 * * * /absolute/path/to/start_scheduler.sh
```

Ensure:

* start_scheduler.sh is executable (chmod +x)
* The Python virtual environment path is correct
* System is awake at 11:00 AM

## 💾 Data Storage Format

The project uses both CSV and HDF5 for persistent storage.

### Why HDF5?

* 🔁 Fast reading/writing of large tables
* 📅 Easy time-based filtering
* 🔒 Deduplication by date
* 🔗 Integrated with pandas.HDFStore

#### HDF5 File Structure

| Data Source      | HDF5 Key      | CSV File              |
| ---------------- | ------------- | --------------------- |
| CoinGecko BTC    | `bitcoin`     | `data/bitcoin.csv`    |
| Open-Meteo       | `weather`     | `data/open_meteo.csv` |
| USGS Earthquakes | `earthquakes` | `data/usgs.csv`       |

## 🗂 Data Structure Example

Example row from open_meteo.csv:

| date       | temperature | wind_speed | weather_code | source         |
| ---------- | ----------- | ---------- | ------------ | -------------- |
| 2025-10-27 | 7.8         | 17.9       | 61           | Open-Meteo API |

## 📊 Visualization

Once data is collected over multiple days, the following graphs are generated:

| Plot                    | Script                     |
| ----------------------- | -------------------------- |
| 📈 Bitcoin Price Trend  | `plotting/plot_bitcoin.py` |
| 🌡️ Temp/Wind in Berlin | `plotting/open_meteo.py`   |
| 🌍 Daily Earthquakes    | `plotting/plot_usgs.py`    |

Each chart includes:

* 📅 Date-based X-axis
* 🏷️ Proper labeling and units (e.g., $, °C, magnitude)
* 🎯 Clean aesthetics and layout
* 🔁 Fallback to .csv if HDF5 fails

## 🧪 Testing & Validation

* Manual insertion of synthetic data for plotting
* Tested fallback to CSV when HDF5 unavailable
* Verified scheduler triggers scraping
* Handled API downtime with retry logic
* Verified deduplication in CSV and HDF5

## ❗ Known Limitations

* 💡 System must be on (not sleeping) at 11:00 AM for cron to run
* 🔌 Internet connection required for scraping APIs
* 🧠 Requires periodic check of scheduler_state.txt
* 🛠️ Scheduler state does not reset automatically after 9 days

## 📦 Requirements

Install via:
```
pip install -r requirements.txt
```
#### Core Dependencies
```
beautifulsoup4==4.14.2
certifi==2025.10.5
charset-normalizer==3.4.4
contourpy==1.3.3
cycler==0.12.1
fonttools==4.60.1
h5py==3.15.1
idna==3.11
kiwisolver==1.4.9
matplotlib==3.10.7
numpy==2.3.4
packaging==25.0
pandas==2.3.3
pandas-stubs==2.3.2.250926
pillow==12.0.0
pyparsing==3.2.5
python-dateutil==2.9.0.post0
pytz==2025.2
requests==2.32.5
schedule==1.2.2
seaborn==0.13.2
six==1.17.0
soupsieve==2.8
typing_extensions==4.15.0
tzdata==2025.2
urllib3==2.5.0
```
## 📄 License

This project was developed for the academic module:
\
Data Quality and Data Wrangling

Python and SQL Programming and Data Analysis
\
IU Internationale Hochschule Akademie

The code is intended strictly for educational use and assessment.
\
Unauthorized reproduction or redistribution is not permitted.

## 📬 Contact
Created by Diana Losch
🔗 GitHub: @dlosch9225