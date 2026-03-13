import h5py
import numpy as np
import matplotlib.pyplot as plt
import rasterio
import xarray as xr
print("Environment Ready")

file_path = r"D:\TMHRS\NISAR\NISAR_L2_PR_GSLC_003_005_D_077_4005_DHDH_A_20251017T132451_20251017T132526_X05007_N_F_J_001.h5"
f = h5py.File(file_path, "r")
print("File opened successfully")

hh = f['science']['LSAR']['GSLC']['grids']['frequencyA']['HH']

print(hh[33400, 34000])
subset = hh[32900:33900, 33500:34500]

import numpy as np
import matplotlib.pyplot as plt
magnitude = np.abs(subset)
power = magnitude**2
power[power <= 0] = np.nan
intensity_db = 10 * np.log10(power)

print("Min dB:", np.nanmin(intensity_db))
print("Max dB:", np.nanmax(intensity_db))
plt.figure(figsize=(6,6))
plt.imshow(intensity_db, cmap='gray', vmin=-30, vmax=5)
plt.colorbar(label="Backscatter (dB)")
plt.title("NISAR L2 GSLC - HH (Subset)")
plt.show()

