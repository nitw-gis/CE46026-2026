# -*- coding: utf-8 -*-
"""
NEON Hyperspectral Reflectance - Working Code
"""

import os
import sys
import requests
import numpy as np
import matplotlib.pyplot as plt


# 1. Function to download files

def download_url(url, download_dir):
    if not os.path.isdir(download_dir):
        os.makedirs(download_dir)
        
    filename = url.split('/')[-1]
    filepath = os.path.join(download_dir, filename)
    
    # avoid re-downloading
    if not os.path.exists(filepath):
        print("Downloading:", filename)
        r = requests.get(url, allow_redirects=True)
        with open(filepath, 'wb') as f:
            f.write(r.content)
    else:
        print("File already exists:", filename)
    
    return filepath



# 2. Download NEON module

module_url = "https://raw.githubusercontent.com/NEONScience/NEON-Data-Skills/main/tutorials/Python/AOP/aop_python_modules/neon_aop_hyperspectral.py"
download_url(module_url, "./python_modules")

# add module path
sys.path.insert(0, "./python_modules")

# import module
import neon_aop_hyperspectral as neon_hs


# 3. Download NEON hyperspectral data 

data_url = "https://storage.googleapis.com/neon-aop-products/2021/FullSite/D02/2021_SERC_5/L3/Spectrometer/Reflectance/NEON_D02_SERC_DP3_368000_4306000_reflectance.h5"

h5_path = download_url(data_url, "./data")



# 4. Read HDF5 data

print("\nReading HDF5 data...\n")

serc_refl, serc_refl_md, wavelengths = neon_hs.aop_h5refl2array(h5_path, 'Reflectance')



# 5. Print metadata

for item in sorted(serc_refl_md):
    print(item + ":", serc_refl_md[item])

print("\nSERC Tile Reflectance Stats:")
print("min:", np.nanmin(serc_refl))
print("max:", round(np.nanmax(serc_refl), 2))
print("mean:", round(np.nanmean(serc_refl), 2))



# 6. Plot a single band (Band 56)

band_index = 55  # python starts from 0

serc_band = serc_refl[:, :, band_index] / serc_refl_md['scale_factor']

neon_hs.plot_aop_refl(
    serc_band,
    serc_refl_md['extent'],
    colorlimit=(0, 0.3),
    title=f"SERC Tile Band {band_index+1}",
    cmap_title="Reflectance",
    colormap='gist_earth'
)



# 7. Plot Spectral Signature 

# choose a pixel (row, col)
row, col = 500, 500

pixel_spectrum = serc_refl[row, col, :] / serc_refl_md['scale_factor']

plt.figure(figsize=(10,5))
plt.plot(wavelengths, pixel_spectrum)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Reflectance")
plt.title(f"Spectral Signature at Pixel ({row},{col})")
plt.grid()
plt.show()
