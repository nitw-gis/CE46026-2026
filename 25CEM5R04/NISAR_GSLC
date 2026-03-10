import h5py
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.windows import Window

# OPEN FILE
file = h5py.File(
    r"E:\NISAR\GSLC\NISAR_L2_PR_GSLC_003_005_D_077_4005_DHDH_A_20251017T132451_20251017T132526_X05007_N_F_J_001.h5","r")

hv = file["/science/LSAR/GSLC/grids/frequencyB/HV"]
x = file["/science/LSAR/GSLC/grids/frequencyB/xCoordinates"]
y = file["/science/LSAR/GSLC/grids/frequencyB/yCoordinates"]

height, width = hv.shape
print("Raster size:", height, width)


# FIX AXIS ORIENTATION
flip_x = False
flip_y = False

if x[0] > x[-1]:
    flip_x = True

if y[0] < y[-1]:
    flip_y = True

xmin = float(min(x[0], x[-1]))
xmax = float(max(x[0], x[-1]))
ymin = float(min(y[0], y[-1]))
ymax = float(max(y[0], y[-1]))

transform = from_bounds(xmin, ymin, xmax, ymax, width, height)

# WRITE GEOTIFF (BLOCK MODE)
with rasterio.open(
    "nisar_hv_backscatter.tif",
    "w",
    driver="GTiff",
    height=height,
    width=width,
    count=1,
    dtype="float32",
    crs="EPSG:32643",  # ← KEEP THIS (your coordinates match UTM Zone 43N)
    transform=transform,
    tiled=True,
    blockxsize=512,
    blockysize=512,
    compress="lzw"
) as dst:

    for i in range(0, height, 512):
        for j in range(0, width, 512):

            row_end = min(i + 512, height)
            col_end = min(j + 512, width)

            # Read ONLY small chunk
            chunk = hv[i:row_end, j:col_end]

            # Apply flips if needed
            if flip_x:
                chunk = np.fliplr(chunk)
            if flip_y:
                chunk = np.flipud(chunk)

            # Convert to dB
            power = np.abs(chunk) ** 2
            power[power == 0] = np.nan
            db = 10 * np.log10(power)
            db = np.clip(db, -30, 10).astype("float32")

            window = Window(
                col_off=j,
                row_off=i,
                width=col_end - j,
                height=row_end - i
            )

            dst.write(db, 1, window=window)

print("GeoTIFF exported successfully")
file.close()
