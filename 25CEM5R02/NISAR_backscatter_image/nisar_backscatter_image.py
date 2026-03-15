#Author: GARNISHA SHREE S K 
#ROLL NO: 25CEM5R02
import h5py
import numpy as np
import matplotlib.pyplot as plt

# ── File path ──────────────────────────────────────────────────────────────
file_path = r"E:\SEM 2\TMHRS\5.NISAR data assignment\nisar_new\NISAR_L2_PR_GSLC_010_165_D_100_2005_DHDH_M_20260120T155930_20260120T155950_X05010_N_P_J_001.h5"

# ── Open file ──────────────────────────────────────────────────────────────
f = h5py.File(file_path, "r")
print("File opened successfully")

# ── Access HH band ─────────────────────────────────────────────────────────
hh = f['science']['LSAR']['GSLC']['grids']['frequencyA']['HH']

print("\n=== HH BAND INFO ===")
print("Rows            :", hh.shape[0])
print("Columns         :", hh.shape[1])
print("Total Pixels    :", f"{hh.shape[0] * hh.shape[1]:,}")

# ── Access coordinates ─────────────────────────────────────────────────────
x_coords = f['science']['LSAR']['GSLC']['grids']['frequencyA']['xCoordinates']
y_coords = f['science']['LSAR']['GSLC']['grids']['frequencyA']['yCoordinates']
x_spacing = f['science']['LSAR']['GSLC']['grids']['frequencyA']['xCoordinateSpacing']
y_spacing = f['science']['LSAR']['GSLC']['grids']['frequencyA']['yCoordinateSpacing']
projection = f['science']['LSAR']['GSLC']['grids']['frequencyA']['projection']

print("\n=== COORDINATE INFO ===")
print("X Coordinates shape :", x_coords.shape)
print("Y Coordinates shape :", y_coords.shape)
print("X Spacing (m)       :", x_spacing[()])
print("Y Spacing (m)       :", y_spacing[()])
print("Projection          :", projection[()])

# ── Define subset (adjust row/col values if needed) ───────────────────────
row_start, row_end = 33500, 34500   # adjust these if image looks wrong
col_start, col_end = 17000, 18000   # adjust these if image looks wrong

subset   = hh[row_start:row_end, col_start:col_end]
x_subset = x_coords[col_start:col_end]
y_subset = y_coords[row_start:row_end]

print("\n=== SUBSET INFO ===")
print("Subset shape  :", subset.shape)
print("X range (m)   :", x_subset[0], "to", x_subset[-1])
print("Y range (m)   :", y_subset[0], "to", y_subset[-1])

# ── Compute backscatter in dB ──────────────────────────────────────────────
magnitude    = np.abs(subset)           # magnitude from complex values
power        = magnitude ** 2           # convert to power
power[power <= 0] = np.nan              # avoid log(0) errors
intensity_db = 10 * np.log10(power)    # convert to dB scale

print("\n=== BACKSCATTER STATS ===")
print("Min dB :", round(np.nanmin(intensity_db), 2))
print("Max dB :", round(np.nanmax(intensity_db), 2))
print("Mean dB:", round(np.nanmean(intensity_db), 2))

# ── Plot ───────────────────────────────────────────────────────────────────
extent = [
    x_subset[0],    # left   (X start)
    x_subset[-1],   # right  (X end)
    y_subset[-1],   # bottom (Y end)
    y_subset[0]     # top    (Y start)
]

plt.figure(figsize=(8, 8))
plt.imshow(intensity_db, cmap='gray', vmin=-30, vmax=5, extent=extent, aspect='auto')
plt.colorbar(label="Backscatter (dB)")
plt.title("NISAR L2 GSLC - HH (Subset)")
plt.xlabel("Easting (m)")
plt.ylabel("Northing (m)")
plt.ticklabel_format(style='sci', axis='both', scilimits=(0, 0))
plt.tight_layout()
plt.savefig("backscattered_image.png", dpi=150, bbox_inches='tight')  # saves image
plt.show()

print("\nImage saved as backscattered_image.png")

# ── Close file ─────────────────────────────────────────────────────────────
f.close()
