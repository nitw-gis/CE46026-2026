# NISAR GSLC HV Backscatter Analysis

## Overview

This project processes **NISAR Level-2 GSLC (Geocoded Single Look Complex) SAR data** to generate an **HV polarization backscatter image**. The workflow reads the NISAR HDF5 dataset, extracts the HV polarization channel, converts the complex SAR data into backscatter intensity (dB), and exports the result as a georeferenced GeoTIFF.

The resulting image helps visualize spatial variations in surface scattering properties such as vegetation structure, terrain roughness, and water bodies.

---

# Mission Overview

The dataset used in this project comes from the **NASA-ISRO Synthetic Aperture Radar (NISAR)** mission.

NISAR is a joint Earth observation mission developed by:

* National Aeronautics and Space Administration (NASA)
* Indian Space Research Organisation (ISRO)

The satellite carries **L-band and S-band Synthetic Aperture Radar (SAR)** instruments designed for monitoring Earth surface processes such as:

* vegetation biomass
* surface deformation
* wetlands
* cryosphere dynamics
* natural hazards

---

# Aim

To extract **HV polarization backscatter** from a NISAR GSLC dataset and generate a georeferenced **backscatter intensity map in decibels (dB)**.

---

# Dataset Information

## Product Identification

**Product Name**

```
NISAR_L2_PR_GSLC_003_005_D_077_4005_DHDH_A_20251017T132451_20251017T132526_X05007_N_F_J_001
```

**Product Type**

Level-2 Geocoded Single Look Complex (GSLC)

**Product Version**

```
NISAR_L2_GSLC_BETA_V1
```

**Data Courtesy**

Jet Propulsion Laboratory (JPL)

---

# Acquisition Details

| Parameter              | Description                   |
| ---------------------- | ----------------------------- |
| Acquisition Start Time | 17 October 2025, 13:24:51 UTC |
| Acquisition Stop Time  | 17 October 2025, 13:25:26 UTC |
| Orbit Direction        | Descending                    |
| Track Number           | 5                             |
| Frame Number           | 77                            |
| CRID                   | X05007                        |
| Joint Observation Only | FALSE                         |

The **descending orbit** indicates that the satellite was moving **from north to south** during acquisition.

---

# Radar Characteristics

| Parameter          | Value      |
| ------------------ | ---------- |
| Frequency Band     | L-band     |
| Main Polarizations | HH, HV     |
| Side Polarizations | HH, HV     |
| Range Bandwidth    | 40 + 5 MHz |

---

# Data Format

The NISAR GSLC dataset is stored in **HDF5 format (.h5)**.

Important datasets used:

```
/science/LSAR/GSLC/grids/frequencyB/HV
/science/LSAR/GSLC/grids/frequencyB/xCoordinates
/science/LSAR/GSLC/grids/frequencyB/yCoordinates
```

These contain:

* **HV complex SAR data**
* **X coordinates (longitude/easting)**
* **Y coordinates (latitude/northing)**

---

# Software and Libraries

Required Python libraries:

* Python 3.x
* NumPy
* h5py
* Rasterio

Install dependencies:

```bash
pip install numpy h5py rasterio
```

---

# Methodology

## 1. Load HDF5 Dataset

The NISAR `.h5` file is opened using **h5py** to access the SAR data.

The following datasets are extracted:

* HV polarization
* X coordinate grid
* Y coordinate grid

---

## 2. Determine Raster Geometry

The coordinate arrays are used to determine:

* raster extent
* spatial orientation
* coordinate bounds

Axis orientation is checked to determine if flipping is required.

---

## 3. Convert SAR Complex Data to Backscatter

SAR data is stored as **complex values**.

Backscatter intensity is computed as:

[
Power = |S|^2
]

Then converted to **decibel scale**:

[
dB = 10 \log_{10}(Power)
]

Values are clipped to a range of:

```
-30 dB to 10 dB
```

This improves visualization.

---

## 4. Block Processing

The raster is processed in **512 × 512 blocks** to reduce memory usage when handling large datasets.

This method allows efficient processing of large SAR scenes.

---

## 5. Export GeoTIFF

The processed backscatter image is exported as:

```
nisar_hv_backscatter.tif
```

Properties:

* CRS: **EPSG:32643 (UTM Zone 43N)**
* Compression: **LZW**
* Tiled raster format

This makes the file compatible with GIS software such as:

* QGIS
* ArcGIS
* SNAP

---

# Output

<img width="940" height="664" alt="image" src="https://github.com/user-attachments/assets/c9088fab-b167-48b1-b628-ea2c292e8901" width="600"/>
<p align="center" >
  <em>Figure 1:NISAR GSLC HV Backscatter image</em>
</p>


---

# Interpretation

The resulting image represents radar return intensity from **HV polarization**.

Key observations:

* **Bright regions** indicate strong backscatter, often associated with:

  * rough surfaces
  * dense vegetation
  * urban structures

* **Dark regions** indicate weak backscatter, typically representing:

  * water bodies
  * smooth surfaces
  * calm terrain

The **reservoir visible in the scene appears dark**, caused by **specular reflection**, where radar signals reflect away from the sensor.

Surrounding vegetation exhibits **moderate backscatter** due to **volume scattering within plant canopies**.

---

# Observations

* Backscatter values range approximately between **-30 dB and -5 dB**.
* These values are consistent with expected **HV polarization responses**.

Characteristics of HV polarization:

* Sensitive to **volume scattering**
* Effective for **vegetation and biomass studies**
* Produces lower backscatter intensity compared to **co-polarized channels (HH)**.

---

# Applications

This workflow can be applied for:

* vegetation and biomass monitoring
* wetland mapping
* land cover classification
* terrain analysis
* hydrological studies
* radar remote sensing research

---

# Author

**Harshidha M**  
Mtech Geoinformatics  
NIT Warangal  
