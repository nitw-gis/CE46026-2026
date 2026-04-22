import h5py
import numpy as np
import matplotlib.pyplot as plt

# Load NEON HDF5 file
file_path = "NEON_reflectance.h5"
hdf = h5py.File(file_path, 'r')

# Explore structure (optional)
print(list(hdf.keys()))

# Access reflectance data
reflectance = hdf['Reflectance']['Reflectance_Data'][:]

# Get wavelengths
wavelengths = hdf['Reflectance']['Metadata']['Spectral_Data']['Wavelength'][:]

# Select a pixel (row, column)
row = 100
col = 100
pixel_spectrum = reflectance[row, col, :]

# Remove invalid values (optional)
pixel_spectrum = np.where(pixel_spectrum == -9999, np.nan, pixel_spectrum)

# Plot spectral reflectance curve
plt.figure()
plt.plot(wavelengths, pixel_spectrum)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Reflectance")
plt.title("Spectral Reflectance Curve (NEON Pixel)")
plt.grid()

plt.show()
