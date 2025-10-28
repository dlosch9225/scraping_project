import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from scrapers.data_utils import load_data

df = load_data("bitcoin.csv", "bitcoin")

# Convert 'date' to datetime and sort
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))

# Unique dates
unique_dates = df["date"].dt.date.unique()

# Plot one continuous line for all dates
ax.plot(df["date"], df["value"], marker='o', color='blue', label="Bitcoin Price")


# Format x-axis
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=0)


# Labels and title
ax.set_title("Bitcoin Price Over Time", fontsize=14, pad=20)
ax.text(1.0, -0.15, "Source: CoinGecko API", transform=ax.transAxes,
        ha='right', va='center', fontsize=9, color='gray')
ax.set_xlabel("Date", fontsize=10, labelpad=10, fontweight='bold')
ax.set_ylabel("Price (USD)", fontsize=10, labelpad=10, fontweight='bold')

ax.set_yticks(range(105000, 114001, 1000))
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x/1000:.0f}k'))
ax.yaxis.grid(True, linestyle='--', alpha=0.5)

# Remove top and right borders (spines)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Legend
ax.legend(title="Day", loc='upper left')
# Legend
ax.legend(loc='upper left', bbox_to_anchor=(0, -0.10), frameon=False)

# Tight layout
plt.tight_layout()

# Show plot
plt.show()
