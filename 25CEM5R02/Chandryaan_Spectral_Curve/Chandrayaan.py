#Author: GARNISHA SHREE S K 
#ROLL NO: 25CEM5R02
import numpy as np
import matplotlib.pyplot as plt
import re


def read_envi_hdr(hdr_path):
    """
    Reads ENVI header file and returns metadata as dictionary
    """
    hdr = {}

    with open(hdr_path, 'r') as f:
        text = f.read()

    # Extract key-value pairs
    for line in text.split('\n'):
        if '=' in line:
            key, val = line.split('=', 1)
            hdr[key.strip().lower()] = val.strip()

    # Extract wavelength values if present
    if 'wavelength' in text.lower():
        wl_text = re.search(r'\{(.*?)\}', text, re.S).group(1)
        hdr['wavelength'] = np.array(
            [float(x) for x in wl_text.replace('\n', '').split(',')]
        )

    return hdr


def read_qub(qub_path, hdr):
    """
    Reads QUB binary file and returns a 3D NumPy array
    (rows, cols, bands)
    """
    samples = int(hdr['samples'])
    lines = int(hdr['lines'])
    bands = int(hdr['bands'])

    # ENVI data type mapping
    data_type_map = {
        '1': np.uint8,
        '2': np.int16,
        '3': np.int32,
        '4': np.float32,
        '5': np.float64
    }

    dtype = data_type_map[hdr['data type']]
    interleave = hdr['interleave'].lower()

    data = np.fromfile(qub_path, dtype=dtype)

    if interleave == 'bsq':
        data = data.reshape((bands, lines, samples))
        cube = np.transpose(data, (1, 2, 0))

    elif interleave == 'bil':
        data = data.reshape((lines, bands, samples))
        cube = np.transpose(data, (0, 2, 1))

    elif interleave == 'bip':
        cube = data.reshape((lines, samples, bands))

    return cube


# File paths (change only this for new datasets)
hdr_file = r"E:\data\calibrated\20210621\ch2_iir_nci_20210621T2245238783_d_img_hw1.hdr"
qub_file = r"E:\data\calibrated\20210621\ch2_iir_nci_20210621T2245238783_d_img_hw1.qub"

# Read data
hdr = read_envi_hdr(hdr_file)
cube = read_qub(qub_file, hdr)

print("Data cube shape (rows, cols, bands):", cube.shape)


# Select pixels (row, column)
pixels = [(50, 60), (120, 140), (200, 100)]

# Wavelength axis
if 'wavelength' in hdr:
    wavelengths = hdr['wavelength']
else:
    wavelengths = np.arange(cube.shape[2])

plt.figure(figsize=(8, 5))

for r, c in pixels:
    spectrum = cube[r, c, :]
    plt.plot(wavelengths, spectrum, label=f'Pixel ({r},{c})')

plt.xlabel("Wavelength (µm)")
plt.ylabel("Reflectance / DN")
plt.title("Spectral Response Curve – Chandrayaan-II")
plt.legend()
plt.grid(True)
plt.show()


