# 🌿 NEON Hyperspectral Data Analysis using Python

## Overview
This project demonstrates how to download, process, and analyze hyperspectral reflectance data from NEON (National Ecological Observatory Network) using Python. The objective is to extract spectral information from a hyperspectral dataset and visualize both spatial and spectral characteristics.

---

## Objectives
- Download NEON hyperspectral reflectance data (.h5 format)
- Read and process HDF5 data using Python
- Visualize a single spectral band as an image
- Extract and plot the spectral signature of a pixel

---

## Dataset
- Source: NEON Airborne Observation Platform (AOP)
- Product: Hyperspectral Surface Reflectance (DP3)
- Format: `.h5` (HDF5)
- Bands: ~426 spectral bands

---

## Technologies & Libraries Used
- Python
- NumPy
- Matplotlib
- Requests
- h5py
- Pandas

---


## Installation & Setup

### 1. Create Conda Environment (optional)
conda create -n neon_env python=3.10
conda activate neon_env
### 2. Install Required Libraries
conda install numpy matplotlib pandas h5py requests


---

## How to Run

1. Run the Python script:
python neon.py


2. The script will:
- Download NEON hyperspectral data
- Load reflectance values
- Display metadata
- Plot a spectral band image
- Generate a spectral signature graph

---

## Outputs

### 1. Reflectance Band Image
- Visualization of a single spectral band (Band 56)

### 2. Spectral Signature Plot
- Reflectance vs Wavelength graph for a selected pixel

---

## Key Concepts

### Hyperspectral Data
- Contains hundreds of narrow spectral bands
- Enables detailed material identification

### Spectral Signature
- Unique reflectance pattern of a material across wavelengths

---

## Notes
- Only **DP3 Reflectance `.h5` files** are compatible with this workflow
- Other NEON products (e.g., DP4) will not work with this code
- Ensure all required Python libraries are installed

---

## Learning Outcome
This project helps in understanding:
- Handling hyperspectral datasets
- Working with HDF5 files in Python
- Extracting and interpreting spectral information

---

## Future Scope
- Apply classification on hyperspectral data
- Compare spectral signatures of different land cover types
- Integrate with remote sensing and GIS workflows

---

## Acknowledgement
Data provided by NEON (National Ecological Observatory Network)

---

## 👩‍💻 Author
Harshidha M

