#step1: Importing h5py and reading the file.
import numpy as np
import rasterio
import h5py
file_path = "C:/Users/LENOVO/Desktop/NISAR_L2_PR_GSLC_003_005_D_077_4005_DHDH_A_20251017T132451_20251017T132526_X05007_N_F_J_001.h5"
with h5py.File(file_path, 'r') as f:
    def print_structure(name, obj):
        print(name)
    f.visititems(print_structure)
  
  #step2: Extracting One Polarization

with h5py.File(file_path, 'r') as f:
    data = f["science/LSAR/GSLC/grids/frequencyA/HH"][:]
print(data.shape)

#step3: Working in tiles(subset) ---- because of memory and system configuration constrains
#finding the valid pixels in the raster

with h5py.File(file_path, 'r') as f:
    hh = f["science/LSAR/GSLC/grids/frequencyA/HH"]
    rows, cols = hh.shape
    found = False
    for i in range(0, rows, 2000):
        for j in range(0, cols, 2000):
            val = hh[i, j]
            if not np.isnan(val.real):
                print("Found valid pixel at:", i, j)
                print("Value:", val)
                found = True
                break
        if found:
            break
    if not found:
        print("No valid pixels found in sparse scan.")

#Step4: Clipping the raster to the valid pixels

row_center = 4000
col_center = 14000
window_size = 1500
row_start = row_center - window_size
row_end   = row_center + window_size
col_start = col_center - window_size
col_end   = col_center + window_size
with h5py.File(file_path, 'r') as f:
    grid = f["science/LSAR/GSLC/grids/frequencyA"]
    hh = grid["HH"]
    subset = hh[row_start:row_end, col_start:col_end]
  
#Step5: Metadata Extraction from GSLC Product

with h5py.File(file_path, 'r') as f:
    print(list(f["science/LSAR/GSLC/grids/frequencyA"].keys()))

#Step6: Reading Metadata

with h5py.File(file_path, 'r') as f:
    grid = f["science/LSAR/GSLC/grids/frequencyA"]

    x_coords = grid["xCoordinates"][:]
    y_coords = grid["yCoordinates"][:]

    x_spacing = grid["xCoordinateSpacing"][()]
    y_spacing = grid["yCoordinateSpacing"][()]

    projection = grid["projection"][()]

print("X spacing:", x_spacing)
print("Y spacing:", y_spacing)
print("Projection:", projection)
print("X min/max:", x_coords.min(), x_coords.max())
print("Y min/max:", y_coords.min(), y_coords.max())


#Step7: Backscatter Conversion

intensity = np.abs(subset)**2
db = 10 * np.log10(intensity + 1e-10)

#Step8: Checking Min, Max and Nan Values

print("NaNs:", np.isnan(db).sum())
print("Min:", np.nanmin(db))
print("Max:", np.nanmax(db))

#Step9: Assigning Nan values in the raster to -9999

clean_db = db.copy()
clean_db[np.isnan(clean_db)] = -9999

with rasterio.open(
    "nisar_HH_valid_subset.tif",
    "w",
    driver="GTiff",
    height=clean_db.shape[0],
    width=clean_db.shape[1],
    count=1,
    dtype=clean_db.dtype,
    crs=crs,
    transform=transform,
    nodata=-9999,
) as dst:
    dst.write(clean_db, 1)

#Step10: Transformation of the coordinates to Geodetic Coordinates

from rasterio.transform import from_origin
from rasterio.crs import CRS

origin_x = x_coords[col_start]
origin_y = y_coords[row_start]

transform = from_origin(
    origin_x,
    origin_y,
    x_spacing,
    abs(y_spacing)
)
crs = CRS.from_epsg(int(projection))

#Step11: Exporting into TIFF file

output_path = "nisar_HH_valid_subset.tif"

with rasterio.open(
    output_path,
    "w",
    driver="GTiff",
    height=clean_db.shape[0],
    width=clean_db.shape[1],
    count=1,
    dtype="float32",     # important
    crs=crs,
    transform=transform,
    nodata=-9999
) as dst:
    dst.write(clean_db.astype("float32"), 1)

print("GeoTIFF exported successfully.")
