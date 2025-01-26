import numpy as np
import h5py
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path
from mpl_toolkits.basemap import Basemap
import sys

# Set up time and date
trenutno_vreme = datetime.now() - timedelta(minutes=12)
zaokruzeno_vreme = trenutno_vreme - timedelta(
    minutes=trenutno_vreme.minute % 15,
    seconds=trenutno_vreme.second,
    microseconds=trenutno_vreme.microsecond
)

mjesec = str(zaokruzeno_vreme.month).zfill(2)
dan = str(zaokruzeno_vreme.day).zfill(2)
sat = str(zaokruzeno_vreme.hour).zfill(2)
minuti = str(zaokruzeno_vreme.minute).zfill(2)
godina = str(zaokruzeno_vreme.year).zfill(4)
dat = godina + mjesec + dan + sat + minuti

# Handle input argument or use default time
if len(sys.argv) > 1:
    datum = sys.argv[1]
else:
    datum = dat

# File path
h5_file_path = f'/home/jay/repos/remote-sensing-2-hail-events/202401/ODC.REF_{datum}.h5'

try:
    # Load the HDF5 file
    f = h5py.File(h5_file_path, 'r')

    # Extract datasets
    ds1 = f['dataset1']['data1']['data'][:, :]  # Reflectivity
    ds2 = f['dataset2']['data1']['data'][:, :]  # QIND (Quality Indicators)

    # Retrieve radar image timestamp from metadata
    startdate = f['dataset1']['what'].attrs['startdate'].decode('utf-8')
    starttime = f['dataset1']['what'].attrs['starttime'].decode('utf-8')
    radar_timestamp = f"{startdate} {starttime[:2]}:{starttime[2:4]}:{starttime[4:6]}"

    # Apply thresholds for hail detection
    dbz_threshold = 65
    dbz_upper_threshold = 80
    qind_threshold = 0.8
    ds1 = np.where(np.isinf(ds1), np.nan, ds1)

    hail_mask = (ds1 >= dbz_threshold) & (ds1 < dbz_upper_threshold) & (ds2 >= qind_threshold) & (~np.isnan(ds1))

    # Basemap settings (from HDF5 metadata or fixed values)
    xscale, xsize, yscale, ysize = 2000.0, 1900, 2000.0, 2200
    LL_lat, LL_lon = 31.746215319325056, -10.434576838640398
    UR_lat, UR_lon = 67.62103710275053, 57.81196475014995

    m = Basemap(
        projection='laea',
        lat_0=55.0, lon_0=10.0,
        llcrnrlat=LL_lat, llcrnrlon=LL_lon,
        urcrnrlat=UR_lat, urcrnrlon=UR_lon,
        resolution='i'
    )

    # Generate Cartesian grid for radar data
    x_coords = np.arange(0, xsize * xscale, xscale)
    y_coords = np.arange(0, ysize * yscale, yscale)[::-1]  # Reverse y for correct orientation
    x_grid, y_grid = np.meshgrid(x_coords, y_coords)

    # Convert Cartesian grid to latitude and longitude using Basemap
    lon_grid, lat_grid = m(x_grid, y_grid, inverse=True)
    
    # Generate hail event list
    hail_events = []
    for i, j in np.argwhere(hail_mask):
        hail_events.append({
            "Radar Image Timestamp": radar_timestamp,
            "Latitude": lat_grid[i, j],
            "Longitude": lon_grid[i, j],
            "DBZH": ds1[i, j]
        })

    # Save hail events to a CSV
    hail_df = pd.DataFrame(hail_events)
    if not hail_df.empty:
        output_csv = "hail_events.csv"
        if Path(output_csv).exists():
            hail_df.to_csv(output_csv, mode='a', header=False, index=False)  
        else:
            hail_df.to_csv(output_csv, mode='w', header=True, index=False)  

        print(f"Hail events detected. Saved to {output_csv}")
    else:
        print("No hail events detected.")

except FileNotFoundError:
    print(f"Error: File not found: {h5_file_path}")
except KeyError as e:
    print(f"Error accessing HDF5 file structure: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
