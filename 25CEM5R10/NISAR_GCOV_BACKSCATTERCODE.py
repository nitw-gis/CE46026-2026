# ==========================================================
# NISAR GCOV Backscatter Extraction and Export to GeoTIFF
# This code reads NISAR GCOV HDF5 data, converts sigma0 to 
# backscatter in dB, visualizes it, and exports it to GeoTIFF
# so it can be opened in ArcGIS or other GIS software.
# ==========================================================

# Import library for reading HDF5 files (NISAR data format)
import h5py

# Import numerical computation library for array operations
import numpy as np

# Import rasterio for creating and writing GeoTIFF raster files
import rasterio

# Import function to define spatial transform of raster
from rasterio.transform import from_origin

# Import matplotlib to visualize the SAR image
import matplotlib.pyplot as plt


# ----------------------------------------------------------
# STEP 1: Specify the path of the NISAR GCOV HDF5 file
# Replace this filename with the location of your NISAR file
# ----------------------------------------------------------

file_path = "NISAR_GCOV_file.h5"


# ----------------------------------------------------------
# STEP 2: Open the NISAR HDF5 file and read datasets
# ----------------------------------------------------------

with h5py.File(file_path, 'r') as f:

    # Print all dataset paths in the file to understand structure
    print("Datasets inside the NISAR file:")

    # Define a function to print dataset names
    def printname(name):
        print(name)

    # Visit all groups and datasets inside the HDF5 file
    f.visit(printname)

    # ------------------------------------------------------
    # Extract sigma0 backscatter data for VV polarization
    # Path may change slightly depending on NISAR product
    # ------------------------------------------------------

    sigma_vv = f['/science/LSAR/GCOV/grids/frequencyA/sigma0_vv'][:]

    # ------------------------------------------------------
    # Extract x and y coordinate arrays of the image grid
    # These represent spatial positions of pixels
    # ------------------------------------------------------

    x = f['/science/LSAR/GCOV/grids/frequencyA/xCoordinates'][:]
    y = f['/science/LSAR/GCOV/grids/frequencyA/yCoordinates'][:]


# ----------------------------------------------------------
# STEP 3: Convert sigma0 to backscatter in decibels (dB)
# SAR backscatter is usually expressed in logarithmic scale
# Formula: Backscatter(dB) = 10 * log10(sigma0)
# ----------------------------------------------------------

sigma_vv_db = 10 * np.log10(sigma_vv)


# ----------------------------------------------------------
# STEP 4: Display the backscatter image using matplotlib
# This helps visualize radar intensity values
# ----------------------------------------------------------

plt.figure(figsize=(8,6))                     # Define size of the plot
plt.imshow(sigma_vv_db, cmap='gray')          # Display raster as grayscale image
plt.colorbar(label='Backscatter (dB)')        # Add colorbar showing dB values
plt.title('NISAR Backscatter VV Polarization')# Add title to the plot
plt.show()                                    # Show the image


# ----------------------------------------------------------
# STEP 5: Calculate pixel size (spatial resolution)
# Difference between adjacent coordinates gives resolution
# ----------------------------------------------------------

pixel_size_x = abs(x[1] - x[0])               # Compute pixel width
pixel_size_y = abs(y[1] - y[0])               # Compute pixel height


# ----------------------------------------------------------
# STEP 6: Create raster transform
# This defines how raster pixels map to geographic space
# ----------------------------------------------------------

transform = from_origin(x.min(), y.max(), pixel_size_x, pixel_size_y)


# ----------------------------------------------------------
# STEP 7: Define output GeoTIFF file name
# ----------------------------------------------------------

output_file = "nisar_backscatter_vv.tif"


# ----------------------------------------------------------
# STEP 8: Export the backscatter image as GeoTIFF
# GeoTIFF format can be directly opened in GIS software
# ----------------------------------------------------------

with rasterio.open(
        output_file,                 # Output file name
        'w',                         # Write mode
        driver='GTiff',              # File format = GeoTIFF
        height=sigma_vv_db.shape[0], # Number of rows in raster
        width=sigma_vv_db.shape[1],  # Number of columns in raster
        count=1,                     # Number of bands (single band)
        dtype=sigma_vv_db.dtype,     # Data type of pixel values
        crs='EPSG:4326',             # Coordinate reference system (WGS84)
        transform=transform          # Spatial transformation matrix
) as dst:

    # Write backscatter array into raster band 1
    dst.write(sigma_vv_db, 1)


# ----------------------------------------------------------
# STEP 9: Print confirmation message
# ----------------------------------------------------------

print("GeoTIFF Exported Successfully: nisar_backscatter_vv.tif")


# ----------------------------------------------------------
# STEP 10: The exported GeoTIFF can now be opened in GIS
# ----------------------------------------------------------

print("You can now open the GeoTIFF in GIS software like ArcGIS.")
