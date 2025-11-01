import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from scrapers.data_utils import load_data

df = load_data("usgs.csv", "earthquakes")

# Convert and group
df["date"] = pd.to_datetime(df["date"])
df_grouped = df.groupby(df["date"].dt.date)["value"].max().reset_index()

# Rename for clarity
df_grouped.columns = ["date", "max_magnitude"]
df_grouped["date"] = pd.to_datetime(df_grouped["date"])

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_grouped["date"], df_grouped["max_magnitude"], color="red", marker="o", linestyle="-", linewidth=2)

# Formatting
ax.set_title("Daily Maximum Earthquake Magnitudes", fontsize=14, pad=20)
ax.set_xlabel("Date", fontsize=10, labelpad=10, fontweight='bold')
ax.set_ylabel("Max Magnitude", fontsize=10, labelpad=10, fontweight='bold')
ax.set_ylim(0, 10)
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.text(1.0, -0.15, "Source: USGS Earthquake Feed", transform=ax.transAxes,
        ha='right', va='center', fontsize=9, color='gray')

ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
plt.xticks(rotation=10)
plt.xticks(fontsize=8)

ax.yaxis.grid(True, linestyle='--', alpha=0.5)
ax.xaxis.grid(False)

# Remove top and right borders (spines)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# ✅ Save to plots directory
os.makedirs("plots", exist_ok=True)
plt.savefig("plots/usgs_plot.png", dpi=300)

# Tight layout
plt.tight_layout()


# Show plot
plt.show()
