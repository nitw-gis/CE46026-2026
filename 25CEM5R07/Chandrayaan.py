import os
import numpy as np
import matplotlib.pyplot as plt

# HDR FILE PATH
hdr_file = r"D:\2 SEM PG Geoinfo\TMHRS\Chandraayan - 2\rim\ch2_iir_nci_20200205T0608264255_d_img_d18.hdr"

print("HDR file:", hdr_file)

# READ HDR FILE
def read_hdr(hdr_file):
    header = {}
    with open(hdr_file, 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                header[key.strip().lower()] = value.strip()
    return header

hdr = read_hdr(hdr_file)

# Print header contents
print("\n--- HDR CONTENTS ---")
for k, v in hdr.items():
    print(k, ":", v)

# LOAD QUB FILE
def load_qub(qub_file, hdr):
    samples = int(hdr['samples'])
    lines = int(hdr['lines'])
    bands = int(hdr['bands'])
    data_type = int(hdr['data type'])

    envi_dtype = {
        1: np.uint8,
        2: np.int16,
        3: np.int32,
        4: np.float32,
        5: np.float64,
        12: np.uint16
    }

    dtype = envi_dtype[data_type]

    data = np.fromfile(qub_file, dtype=dtype)

    cube = data.reshape((bands, lines, samples))
    cube = np.transpose(cube, (1, 2, 0))  # (rows, cols, bands)

    return cube

# QUB FILE PATH
qub_file = r"D:\2 SEM PG Geoinfo\TMHRS\Chandraayan - 2\rim\ch2_iir_nci_20200205T0608264255_d_img_d18.qub"

cube = load_qub(qub_file, hdr)

print("\nCube shape:", cube.shape)

# WAVELENGTHS
if 'wavelength' in hdr:
    wavelengths = np.array(
        [float(w) for w in hdr['wavelength']
         .replace('{', '')
         .replace('}', '')
         .split(',')]
    )
else:
    wavelengths = np.arange(cube.shape[2])

print("Number of wavelengths:", len(wavelengths))

# SPECTRAL PLOTS
pixels = [(50, 50), (100, 100), (150, 150)]

plt.figure(figsize=(10, 6))
for (r, c) in pixels:
    plt.plot(wavelengths, cube[r, c, :], label=f"Pixel ({r},{c})")

plt.xlabel("Wavelength")
plt.ylabel("Radiance / Reflectance")
plt.title("Chandrayaan-2 IIRS Spectral Curve")
plt.legend()
plt.grid(True)
plt.show()

