#  NEON-National Ecological Observatory Network 

Source: NEON Data Portal
The dataset provides:
Surface directional reflectance Orthorectified hyperspectral imagery  (UTM projection)
426 spectral bands
1 km × 1 km mosaicked tiles
Atmospheric

It is distributed in an open HDF5 format including all 426 bands from the NEON Imaging Spectrometer. 

It is calibrated, atmospherically corrected, mosaicked, and distributed as scaled reflectance.

# 🌿 Spectral Curve Analysis using NEON Hyperspectral Data

## 📌 Overview
This project demonstrates extraction and analysis of spectral reflectance curves using hyperspectral data from the NEON Airborne Observation Platform (AOP).

The study uses high-resolution hyperspectral imagery to analyze surface reflectance behavior across wavelengths and identify characteristic signatures of vegetation.

---

## 🛰️ Dataset
- Source: NEON (National Ecological Observatory Network)
- Product: DP3.30006.001 – Surface Directional Reflectance (Mosaic)
- Site: AL-D08-TALL (Talladega National Forest, Alabama, USA)
- Data Type: Hyperspectral (HDF5 format)
- Bands: ~426 spectral bands
- Spectral Range: ~380 nm – 2500 nm
- Spatial Resolution: 1 m (approx.)

---

## 🎯 Objectives
- Extract spectral reflectance values from hyperspectral data
- Plot spectral curves (reflectance vs wavelength)
- Analyze vegetation spectral signature
- Understand red-edge behavior

---

## ⚙️ Methodology

### 1. Data Acquisition
- Selected NEON site: AL-D08-TALL
- Downloaded one hyperspectral tile (.h5)

### 2. Data Processing
- Loaded HDF5 data using Python (h5py)
- Extracted reflectance cube
- Retrieved wavelength information

### 3. Spectral Extraction
- Selected pixel coordinates
- Extracted spectral profile across all bands

### 4. Visualization
- Plotted reflectance vs wavelength curves using matplotlib

---

## 📈 Spectral Curve Concept

Spectral curves represent how a surface reflects electromagnetic radiation across different wavelengths.

Vegetation typically shows:
- Low reflectance in blue and red regions
- Peak in green region
- Sharp increase in near-infrared (red-edge)

---

## 🛠️ Tools & Libraries
- Python
- h5py
- numpy
- matplotlib
- QGIS (optional visualization)

---

