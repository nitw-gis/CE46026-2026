"""
Author: Charvi Sree
Roll Number: 25CEM5R06
Course: CE46026 - Thermal, Microwave and Hyperspectral Remote Sensing

Description:
This script reads radar backscatter data (NISAR SAR data) and displays
the backscatter image using Python. The script loads the raster dataset
and visualizes radar backscatter using matplotlib.
"""

import rasterio
import matplotlib.pyplot as plt

# Path to SAR backscatter raster
file_path = "nisar_backscatter.tif"

# Open raster dataset
with rasterio.open(file_path) as dataset:

    backscatter = dataset.read(1)

    plt.figure(figsize=(8,6))
    plt.imshow(backscatter, cmap='gray')

    plt.title("NISAR SAR Backscatter Image")
    plt.colorbar(label="Backscatter Intensity")

    plt.xlabel("Pixels")
    plt.ylabel("Pixels")

    plt.show()
