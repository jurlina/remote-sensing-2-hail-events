import numpy as np
from mpl_toolkits.basemap import Basemap
from pyproj import Proj, Transformer

# Metadata from HDF5 file
xscale, xsize, yscale, ysize = 2000.0, 1900, 2000.0, 2200
LL_lat, LL_lon = 31.746215319325056, -10.434576838640398  # Lower-left corner
UR_lat, UR_lon = 67.62103710275053, 57.81196475014995    # Upper-right corner
proj_def = "+proj=laea +lat_0=55.0 +lon_0=10.0 +units=m +ellps=WGS84"

# Create Basemap instance
m = Basemap(
    projection='laea',
    lat_0=55.0, lon_0=10.0,
    llcrnrlat=LL_lat, llcrnrlon=LL_lon,
    urcrnrlat=UR_lat, urcrnrlon=UR_lon,
    resolution='i'
)

# Generate Cartesian grid for radar data
x = np.arange(0, xsize * xscale, xscale)
y = np.arange(0, ysize * yscale, yscale)[::-1]
x_grid, y_grid = np.meshgrid(x, y)

# Convert Cartesian grid to latitude and longitude using Basemap
lon_grid_basemap, lat_grid_basemap = m(x_grid, y_grid, inverse=True)

# Define pyproj Transformer (from LAEA to WGS84, without offsets)
proj = Proj(proj_def)
transformer = Transformer.from_proj(proj, "epsg:4326", always_xy=True)

# Convert Cartesian grid to latitude and longitude using pyproj
lon_grid_pyproj, lat_grid_pyproj = transformer.transform(x_grid, y_grid)

# Compare the results
print("Latitude grid shape (Basemap):", lat_grid_basemap.shape)
print("Longitude grid shape (Basemap):", lon_grid_basemap.shape)

# Check Basemap corner coordinates
print("\nBasemap Corners:")
print("Lower-left lat/lon (Basemap):", lat_grid_basemap[-1, 0], lon_grid_basemap[-1, 0])
print("Lower-right lat/lon (Basemap):", lat_grid_basemap[-1, -1], lon_grid_basemap[-1, -1])
print("Upper-left lat/lon (Basemap):", lat_grid_basemap[0, 0], lon_grid_basemap[0, 0])
print("Upper-right lat/lon (Basemap):", lat_grid_basemap[0, -1], lon_grid_basemap[0, -1])

# Check pyproj corner coordinates
print("\npyproj Corners:")
print("Lower-left lat/lon (pyproj):", lat_grid_pyproj[-1, 0], lon_grid_pyproj[-1, 0])
print("Lower-right lat/lon (pyproj):", lat_grid_pyproj[-1, -1], lon_grid_pyproj[-1, -1])
print("Upper-left lat/lon (pyproj):", lat_grid_pyproj[0, 0], lon_grid_pyproj[0, 0])
print("Upper-right lat/lon (pyproj):", lat_grid_pyproj[0, -1], lon_grid_pyproj[0, -1])
