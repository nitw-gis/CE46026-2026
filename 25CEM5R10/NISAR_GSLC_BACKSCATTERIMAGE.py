# ===============================================================
# NISAR GSLC Backscatter Processing and Export to GeoTIFF
#
# This script reads a NISAR GSLC HDF5 file, extracts radar data,
# computes the radar backscatter intensity, converts it into
# decibel (dB) scale, visualizes the result, and exports the
# processed image as a GeoTIFF file that can be opened in GIS
# software such as ArcGIS or QGIS.
#
# GSLC stands for Geocoded Single Look Complex product.
# It contains complex SAR data (real and imaginary components)
# that represent radar amplitude and phase information.
#
# The workflow performed in this code:
# 1. Load required Python libraries
# 2. Open the NISAR GSLC HDF5 file
# 3. Explore the dataset structure
# 4. Extract complex SAR data (VV polarization)
# 5. Compute radar intensity from complex values
# 6. Convert intensity to backscatter in decibel scale
# 7. Visualize the radar image
# 8. Compute spatial resolution from coordinate arrays
# 9. Create georeferencing transform
# 10. Export the processed image as a GeoTIFF raster
# ===============================================================


# ---------------------------------------------------------------
# Import libraries required for radar data processing
# ---------------------------------------------------------------

# h5py library is used to read HDF5 files such as NISAR products
import h5py

# numpy is used for numerical calculations and array operations
import numpy as np

# rasterio is used for writing geospatial raster files (GeoTIFF)
import rasterio

# function used to define spatial reference transform of raster
from rasterio.transform import from_origin

# matplotlib is used to visualize the SAR image in Jupyter
import matplotlib.pyplot as plt


# ---------------------------------------------------------------
# Step 1: Define the path of the NISAR GSLC data file
# Replace the filename below with your GSLC file location
# ---------------------------------------------------------------

file_path = "NISAR_GSLC_file.h5"


# ---------------------------------------------------------------
# Step 2: Open the GSLC file in read mode
# ---------------------------------------------------------------

# 'with' statement ensures the file is automatically closed
# after reading, preventing memory issues
with h5py.File(file_path, 'r') as f:

    # Print message to indicate dataset listing
    print("Datasets inside the NISAR GSLC file:")

    # Function to print dataset names
    # It will be used to explore the internal structure
    def printname(name):
        print(name)

    # Visit every group and dataset inside the HDF5 file
    # This helps identify where radar data is stored
    f.visit(printname)

    # -----------------------------------------------------------
    # Step 3: Extract complex SAR data for VV polarization
    #
    # GSLC data contains complex values representing
    # radar amplitude and phase.
    #
    # Complex number format:
    # S = Real + i(Imaginary)
    #
    # Backscatter intensity is derived from the magnitude
    # of the complex number.
    # -----------------------------------------------------------

    complex_data = f['/science/LSAR/GSLC/grids/frequencyA/VV'][:]

    # -----------------------------------------------------------
    # Step 4: Extract coordinate arrays
    #
    # These arrays store the spatial grid coordinates
    # of the radar image pixels.
    #
    # They are required to correctly georeference
    # the exported raster image.
    # -----------------------------------------------------------

    x = f['/science/LSAR/GSLC/grids/frequencyA/xCoordinates'][:]
    y = f['/science/LSAR/GSLC/grids/frequencyA/yCoordinates'][:]


# ---------------------------------------------------------------
# Step 5: Compute radar intensity
#
# GSLC data is complex-valued (real + imaginary).
# Radar intensity is calculated using the magnitude squared.
#
# Intensity = |S|²
# where S is the complex radar signal.
# ---------------------------------------------------------------

intensity = np.abs(complex_data) ** 2


# ---------------------------------------------------------------
# Step 6: Convert radar intensity to backscatter in decibels
#
# Radar backscatter is usually expressed in logarithmic scale:
#
# Backscatter (dB) = 10 * log10(Intensity)
#
# This conversion compresses the dynamic range and
# makes the radar image easier to interpret.
# ---------------------------------------------------------------

backscatter_db = 10 * np.log10(intensity)


# ---------------------------------------------------------------
# Step 7: Visualize the backscatter image
#
# The radar image is displayed as a grayscale image
# where brighter pixels represent stronger reflections.
# ---------------------------------------------------------------

plt.figure(figsize=(8,6))                         # Create figure window
plt.imshow(backscatter_db, cmap='gray')           # Display radar image
plt.colorbar(label='Backscatter (dB)')            # Add scale bar
plt.title('NISAR GSLC Backscatter (VV Polarization)')
plt.show()                                        # Show the image


# ---------------------------------------------------------------
# Step 8: Calculate pixel resolution
#
# Pixel size is determined by the difference between
# consecutive coordinate values.
# ---------------------------------------------------------------

pixel_size_x = abs(x[1] - x[0])                   # Horizontal resolution
pixel_size_y = abs(y[1] - y[0])                   # Vertical resolution


# ---------------------------------------------------------------
# Step 9: Create spatial transformation
#
# The transform defines how pixel coordinates
# correspond to real-world geographic coordinates.
# ---------------------------------------------------------------

transform = from_origin(x.min(), y.max(),
                        pixel_size_x, pixel_size_y)


# ---------------------------------------------------------------
# Step 10: Define output GeoTIFF file name
# ---------------------------------------------------------------

output_file = "nisar_gslc_backscatter_vv.tif"


# ---------------------------------------------------------------
# Step 11: Export the processed radar image as GeoTIFF
#
# GeoTIFF stores both raster data and spatial metadata.
# This allows the file to be directly opened in GIS software.
# ---------------------------------------------------------------

with rasterio.open(
        output_file,                       # Output raster file
        'w',                               # Write mode
        driver='GTiff',                    # GeoTIFF format
        height=backscatter_db.shape[0],    # Number of rows
        width=backscatter_db.shape[1],     # Number of columns
        count=1,                           # Single raster band
        dtype=backscatter_db.dtype,        # Data type
        crs='EPSG:4326',                   # Coordinate system (WGS84)
        transform=transform                # Spatial transformation
) as dst:

    # Write the backscatter array to raster band 1
    dst.write(backscatter_db, 1)


# ---------------------------------------------------------------
# Step 12: Display completion message
# ---------------------------------------------------------------

print("GeoTIFF Exported Successfully: nisar_gslc_backscatter_vv.tif")
print("The file can now be opened in GIS software.")
