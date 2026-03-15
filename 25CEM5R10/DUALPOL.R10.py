# -------------------------------------------------------------
# STEP 1: IMPORT REQUIRED LIBRARIES
# -------------------------------------------------------------

# h5py is used to read HDF5 files. NISAR GSLC data is stored in HDF5 format.
import h5py

# numpy is used for numerical calculations such as magnitude, squaring and logarithms
import numpy as np

# rasterio is used to write geospatial raster data (GeoTIFF) which can be opened in QGIS
import rasterio

# matplotlib is used to visualize the SAR backscatter images
import matplotlib.pyplot as plt


# -------------------------------------------------------------
# STEP 2: DEFINE INPUT FILE PATH
# -------------------------------------------------------------

# Path to the NISAR GSLC HDF5 file
# Replace this with the location of your downloaded NISAR GSLC data
file_path = "NISAR_GSLC_file.h5"


# -------------------------------------------------------------
# STEP 3: OPEN THE NISAR GSLC FILE
# -------------------------------------------------------------

# Open the HDF5 file in read mode ('r')
# This allows us to access the datasets stored inside the file
f = h5py.File(file_path, 'r')


# -------------------------------------------------------------
# STEP 4: ACCESS POLARIZATION DATASETS
# -------------------------------------------------------------

# NISAR GSLC stores SAR data in groups following a directory structure.
# The path below corresponds to Frequency A polarization grids.

# VV polarization complex SAR data
vv_complex = f['/science/LSAR/GSLC/grids/frequencyA/VV'][:]

# VH polarization complex SAR data
vh_complex = f['/science/LSAR/GSLC/grids/frequencyA/VH'][:]

# Each pixel here is a complex number: (real + imaginary part)
# Example pixel value: a + bj


# -------------------------------------------------------------
# STEP 5: CONVERT COMPLEX DATA TO INTENSITY
# -------------------------------------------------------------

# SAR backscatter is derived from the magnitude of the complex signal.
# The magnitude of a complex number is:
# magnitude = sqrt(real^2 + imag^2)

# Intensity is magnitude squared:
# intensity = |S|^2

vv_intensity = np.abs(vv_complex)**2
vh_intensity = np.abs(vh_complex)**2


# -------------------------------------------------------------
# STEP 6: CONVERT INTENSITY TO BACKSCATTER IN dB
# -------------------------------------------------------------

# SAR images are usually represented in decibels (dB)

# Formula:
# backscatter_dB = 10 * log10(intensity)

# Small value (1e-10) added to avoid log(0) errors
vv_backscatter_db = 10 * np.log10(vv_intensity + 1e-10)
vh_backscatter_db = 10 * np.log10(vh_intensity + 1e-10)


# -------------------------------------------------------------
# STEP 7: STACK BOTH POLARIZATIONS
# -------------------------------------------------------------

# Create a dual polarization stack
# Band 1 → VV
# Band 2 → VH

dual_pol_stack = np.stack((vv_backscatter_db, vh_backscatter_db))


# -------------------------------------------------------------
# STEP 8: DEFINE OUTPUT GEOTIFF FILE
# -------------------------------------------------------------

# Name of output raster file
output_file = "nisar_dual_pol_backscatter.tif"


# -------------------------------------------------------------
# STEP 9: WRITE THE DATA AS A GEOTIFF FILE
# -------------------------------------------------------------

# Open a new GeoTIFF file for writing

with rasterio.open(
        output_file,              # Output file name
        'w',                      # Write mode
        driver='GTiff',           # GeoTIFF format
        height=vv_backscatter_db.shape[0],  # Number of rows
        width=vv_backscatter_db.shape[1],   # Number of columns
        count=2,                  # Number of bands (VV and VH)
        dtype='float32'           # Data type
) as dst:

    # Write VV backscatter to Band 1
    dst.write(vv_backscatter_db.astype('float32'), 1)

    # Write VH backscatter to Band 2
    dst.write(vh_backscatter_db.astype('float32'), 2)


# -------------------------------------------------------------
# STEP 10: CONFIRM EXPORT
# -------------------------------------------------------------

print("Dual polarization backscatter GeoTIFF exported successfully!")


# -------------------------------------------------------------
# STEP 11: VISUALIZE BACKSCATTER IMAGES
# -------------------------------------------------------------

# Create a figure window
plt.figure(figsize=(10,4))

# Display VV backscatter
plt.subplot(1,2,1)
plt.imshow(vv_backscatter_db, cmap='gray')
plt.title("VV Backscatter (dB)")
plt.colorbar()

# Display VH backscatter
plt.subplot(1,2,2)
plt.imshow(vh_backscatter_db, cmap='gray')
plt.title("VH Backscatter (dB)")
plt.colorbar()

# Show the plots
plt.show()


# -------------------------------------------------------------
# STEP 12: CLOSE THE HDF5 FILE
# -------------------------------------------------------------

# Always close files after processing
f.close()
