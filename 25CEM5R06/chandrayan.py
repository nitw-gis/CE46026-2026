"""
Author: Charvi Sree
Roll Number: YOUR_ROLL_NUMBER
Course: CE46026 - Thematic Remote Sensing
Assignment: Chandrayaan-II Hyperspectral Data Plotting

Description:
This script reads Chandrayaan-II IIRS calibrated hyperspectral data
(.qub data cube) using the associated .hdr file. The hyperspectral cube
is converted into a 3D NumPy array and spectral responses for selected
pixels are plotted using matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt
import spectral as sp

# ---------------------------------------------------
# Step 1: Define paths
# ---------------------------------------------------

hdr_path = r"D:\NTW\sem_2\THMRS\chandrayan\ch2_iir_nci_20250729T0936115604_d_img_d18\data\calibrated\20250729\ch2_iir_nci_20250729T0936115604_d_img_d18.hdr"

qub_path = r"D:\NTW\sem_2\THMRS\chandrayan\ch2_iir_nci_20250729T0936115604_d_img_d18\data\calibrated\20250729\ch2_iir_nci_20250729T0936115604_d_img_d18.qub"


# ---------------------------------------------------
# Step 2: Open hyperspectral cube
# ---------------------------------------------------

img = sp.io.envi.open(hdr_path, qub_path)

cube = img.load()

print("Cube loaded successfully")
print("Cube shape:", cube.shape)


# ---------------------------------------------------
# Step 3: Display one spectral band
# ---------------------------------------------------

band_number = 10

plt.figure(figsize=(6,6))
plt.imshow(cube[:, :, band_number], cmap='gray')
plt.title(f"Band {band_number}")
plt.colorbar()
plt.show()

# ---------------------------------------------------
# Step 4: Spectral response for pixel
# ---------------------------------------------------
row = 100
col = 120

# Extract spectrum
spectrum = cube[row, col, :]

# Convert to 1D array
spectrum = np.array(spectrum).flatten()

plt.figure(figsize=(8,5))
plt.plot(spectrum)

plt.xlabel("Spectral Band")
plt.ylabel("Reflectance")
plt.title(f"Spectral Response of Pixel ({row},{col})")

plt.show()


# ---------------------------------------------------
# Step 5: Spectral response for multiple pixels
# ---------------------------------------------------
pixels = [(50,50),(100,120),(200,200),(300,150)]

plt.figure(figsize=(8,5))

for r,c in pixels:

    spectrum = cube[r,c,:]
    spectrum = np.array(spectrum).flatten()

    plt.plot(spectrum,label=f"Pixel {r},{c}")

plt.xlabel("Spectral Band")
plt.ylabel("Reflectance")
plt.title("Spectral Response Comparison")

plt.legend()

plt.show()
