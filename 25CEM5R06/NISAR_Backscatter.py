"""
Author: Charvi Sree
Roll Number: 25CEM5R06
Course: CE46026 – THERMAL MICROWAVE AND HYPERSPECTRAL Remote Sensing

Description:
This script reads NISAR GCOV SAR data stored in HDF5 format and
visualizes the radar backscatter image. The VV polarization
covariance term (VVVV) is extracted and converted to magnitude
for visualization.

The script also downsamples the raster to reduce memory usage
and plots the SAR backscatter image using matplotlib.
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------
# Path to NISAR HDF5 file
# ------------------------------------
file_path = r"D:\NTW\sem_2\THMRS\NISAR\NISAR_L2_PR_GCOV_010_164_D_077_2005_QPDH_A_20260120T140632_20260120T140648_X05010_N_P_J_001.h5"



# ------------------------------------
# Open HDF5 file
# ------------------------------------
file = h5py.File(file_path, 'r')


# ------------------------------------
# Load VV polarization covariance data
# ------------------------------------
dataset = file['science/LSAR/GCOV/grids/frequencyA/VVVV']

backscatter = dataset[:]


# ------------------------------------
# Convert complex values to magnitude
# ------------------------------------
backscatter_mag = np.abs(backscatter)


# ------------------------------------
# Downsample data for visualization
# ------------------------------------
backscatter_mag = backscatter_mag[::10, ::10]


print("Backscatter data shape:", backscatter_mag.shape)


# ------------------------------------
# Convert to decibel scale
# ------------------------------------
backscatter_db = 10 * np.log10(backscatter_mag + 1e-10)


# ------------------------------------
# Improve visualization contrast
# ------------------------------------
vmin = np.percentile(backscatter_db, 2)
vmax = np.percentile(backscatter_db, 98)


# ------------------------------------
# Plot SAR backscatter image
# ------------------------------------
plt.figure(figsize=(8,6))

plt.imshow(backscatter_db, cmap='gray', vmin=vmin, vmax=vmax)

plt.title("NISAR SAR Backscatter (VV Polarization)")
plt.colorbar(label="Backscatter (dB)")

plt.xlabel("Pixels")
plt.ylabel("Pixels")

plt.show()


# reduce size for memory
data = data[::10, ::10]

# read coordinates
x = f['science/LSAR/GCOV/grids/frequencyA/xCoordinates'][:]
y = f['science/LSAR/GCOV/grids/frequencyA/yCoordinates'][:]

xmin, xmax = x.min(), x.max()
ymin, ymax = y.min(), y.max()

transform = from_bounds(xmin, ymin, xmax, ymax, data.shape[1], data.shape[0])

# export GeoTIFF (without CRS to avoid error)
with rasterio.open(
    "nisar3_backscatter.tif",
    "w",
    driver="GTiff",
    height=data.shape[0],
    width=data.shape[1],
    count=1,
    dtype=data.dtype,
    transform=transform,
) as dst:
    dst.write(data,1)

print("GeoTIFF created")
