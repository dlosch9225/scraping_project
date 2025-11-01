import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scrapers.data_utils import load_data

df = load_data("open_meteo.csv", "weather")

# Convert 'date' column to datetime
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Plotting both temperature and wind speed
fig, ax = plt.subplots(figsize=(10, 5))

# Temperature line
ax.plot(df["date"], df["temperature"], label="Temperature (°C)", marker='o', color='orange')

# Wind speed line
ax.plot(df["date"], df["wind_speed"], label="Wind Speed (km/h)", marker='s', color='blue')

# Format x-axis
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
plt.xticks(rotation=10)
plt.xticks(fontsize=8)

# Labels and title
ax.set_title("Weather in Berlin: Temperature and Wind Speed", fontsize=14, pad=20)
ax.set_xlabel("Date", fontsize=10, labelpad=10, fontweight='bold')
ax.set_ylabel("Value (km/h,°C)", fontsize=10, labelpad=10, fontweight='bold')
ax.set_ylim(0, 50)
ax.text(1.0, -0.15, "Source: Open-Meteo API", transform=ax.transAxes,
        ha='right', va='center', fontsize=9, color='gray')
ax.yaxis.grid(True, linestyle='--', alpha=0.5)

# Remove top and right borders (spines)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Legend
ax.legend(loc='upper left', bbox_to_anchor=(0, -0.10), frameon=False)

# Tight layout
plt.tight_layout()


# ✅ Save to plots directory
os.makedirs("plots", exist_ok=True)
plt.savefig("plots/open_meteo_plot.png", dpi=300)

# Show plot
plt.show()