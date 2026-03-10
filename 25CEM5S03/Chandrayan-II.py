from spectral import envi
import numpy as np
import matplotlib.pyplot as plt
import os

qub_path = r"G:\2809\Desktop filess\Assignments\Sem-2\TMHRS\ASSIGNEMENT02\data\calibrated\20220710\ch2_iir_nci_20220710T2224274587_d_img_hw1.qub"
hdr_path = r"G:\2809\Desktop filess\Assignments\Sem-2\TMHRS\ASSIGNEMENT02\data\calibrated\20220710\ch2_iir_nci_20220710T2224274587_d_img_hw1.hdr"

print("QUB exists:", os.path.exists(qub_path))
print("HDR exists:", os.path.exists(hdr_path))

if not (os.path.exists(qub_path) and os.path.exists(hdr_path)):
    raise FileNotFoundError(" QUB or HDR file not found. Check paths!")

img = envi.open(hdr_path, qub_path)

print("\nMetadata keys:")
print(img.metadata.keys())

cube = img.load()
print("\nCube shape (Lines, Samples, Bands):", cube.shape)

row = 4000     
col = 120      

spectrum = img.read_pixel(row, col)
spectrum = np.array(spectrum)

print("\nSpectrum shape:", spectrum.shape)

bands = np.arange(len(spectrum))

plt.figure(figsize=(9, 5))
plt.plot(bands, spectrum, linewidth=1.5)
plt.xlabel("Band Number")
plt.ylabel("Radiance")
plt.title("Chandrayaan-2 IIR Spectral Radiance Curve")
plt.grid(True)
plt.tight_layout()
plt.show()

print("\n Spectral extract
