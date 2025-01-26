import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# # Check for command-line arguments
# if len(sys.argv) != 2:
#     print("Usage: python plot.py YYYYMMDDHHMM")
#     sys.exit(1)

# # Parse the timestamp from the command-line argument
# timestamp = sys.argv[1]
csv_file = f"hail_events.csv"

# Step 1: Read the CSV file
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    print(f"Error: File not found: {csv_file}")
    sys.exit(1)

# Ensure necessary columns exist
if not {"Latitude", "Longitude", "DBZH"}.issubset(df.columns):
    print("Error: CSV file must contain 'Latitude', 'Longitude', and 'DBZH' columns.")
    sys.exit(1)

# Step 2: Define grid domain
min_lat, max_lat = df["Latitude"].min(), df["Latitude"].max()
min_lon, max_lon = df["Longitude"].min(), df["Longitude"].max()

# Expand bounds slightly to ensure all points fit
lat_padding = 2
lon_padding = 2
min_lat -= lat_padding
max_lat += lat_padding
min_lon -= lon_padding
max_lon += lon_padding

print(f"Map bounds: lat({min_lat}, {max_lat}), lon({min_lon}, {max_lon})")


# Step 3: Create a 2 km resolution grid
grid_resolution = 0.02  # Approx ~2 km
lats = np.arange(min_lat, max_lat, grid_resolution)
lons = np.arange(min_lon, max_lon, grid_resolution)
lon_grid, lat_grid = np.meshgrid(lons, lats)

# Step 4: Initialize Basemap
fig, ax = plt.subplots(figsize=(12, 10))
m = Basemap(projection='merc',
            llcrnrlat=min_lat, urcrnrlat=max_lat,
            llcrnrlon=min_lon, urcrnrlon=max_lon,
            resolution='i', ax=ax)

m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='lightgray', lake_color='aqua')
m.drawmapboundary(fill_color='aqua')

# Step 5: Plot hail events as red squares
for _, row in df.iterrows():
    x, y = m(row["Longitude"], row["Latitude"])  # Convert lat/lon to map coordinates
    ax.scatter(x, y, s=20, color="red", marker="s", edgecolor="black", label="Hail Event")

# Avoid duplicate labels in the legend
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())

# Step 6: Finalize and Save the Plot
plt.title(f"Hail Events", fontsize=16)
output_plot = f"./images/hail_events.png"
plt.savefig(output_plot, dpi=300, bbox_inches="tight")
plt.show()

print(f"Plot saved to {output_plot}")
