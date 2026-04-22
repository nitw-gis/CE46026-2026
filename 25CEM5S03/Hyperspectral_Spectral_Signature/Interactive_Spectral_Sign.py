import h5py

file_path = r"G:\2809\Desktop filess\Assignments\Sem-2\TMHRS\Hyperspectral\NEON_refl-surf-dir-ortho-mosaic\NEON.D01.HARV.DP3.30006.001.2014-06.basic.20260422T135545Z.RELEASE-2026\NEON_D01_HARV_DP3_723000_4706000_reflectance.h5"

with h5py.File(file_path, 'r') as f:
    def print_structure(name, obj):
        print(name)
    f.visititems(print_structure)

import numpy as np

with h5py.File(file_path, 'r') as f:
    refl = f['HARV/Reflectance/Reflectance_Data'][:]
    wavelengths = f['HARV/Reflectance/Metadata/Spectral_Data/Wavelength'][:]

scale_factor = 10000.0
refl = refl / scale_factor

import matplotlib.pyplot as plt

pixel_x = 100
pixel_y = 100

spectrum = refl[pixel_y, pixel_x, :]

plt.plot(wavelengths, spectrum)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Reflectance")
plt.title(f"Spectral Signature at ({pixel_x},{pixel_y})")
plt.show()


from ipywidgets import interact, IntText

interact(
    interactive_spectra_plot,
    x=IntText(value=100, description='X:'),
    y=IntText(value=100, description='Y:')
)

def find_band(target):
    return np.argmin(np.abs(wavelengths - target))

r = refl[:, :, find_band(660)]
g = refl[:, :, find_band(550)]
b = refl[:, :, find_band(470)]

rgb = np.stack([r, g, b], axis=2)

# Normalize
rgb = (rgb - np.min(rgb)) / (np.max(rgb) - np.min(rgb))

plt.imshow(rgb)
plt.title("RGB Composite")
plt.axis('off')
plt.show()

import matplotlib.pyplot as plt
from ipywidgets import interact_manual, BoundedIntText

def show_pixel_spectrum(x, y):
    fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    
    # LEFT: Image with selected pixel
    ax[0].imshow(rgb)
    ax[0].scatter(x, y, color='red', s=40)
    ax[0].set_title(f"Pixel Location (x={x}, y={y})")
    ax[0].axis('off')
    
    # RIGHT: Spectral signature
    spectrum = refl[y, x, :]
    ax[1].plot(wavelengths, spectrum)
    ax[1].set_xlabel("Wavelength (nm)")
    ax[1].set_ylabel("Reflectance")
    ax[1].set_title("Spectral Signature")
    ax[1].grid()
    
    plt.show()
from ipywidgets import interact, BoundedIntText

interact(
    show_pixel_spectrum,
    x=BoundedIntText(value=100, min=0, max=refl.shape[1]-1, description='X:'),
    y=BoundedIntText(value=100, min=0, max=refl.shape[0]-1, description='Y:')
)
