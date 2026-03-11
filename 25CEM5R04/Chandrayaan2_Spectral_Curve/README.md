# Chandrayaan-2 IIRS Spectral Curve Analysis

## Overview

This project extracts and analyzes spectral responses from **Chandrayaan-2 IIRS (Imaging Infrared Spectrometer) hyperspectral data** using Python. The goal is to visualize how radiance varies across different wavelengths for selected pixels on the lunar surface.

Hyperspectral datasets contain hundreds of spectral bands, allowing detailed analysis of surface composition. By plotting spectral curves, we can study how different lunar materials respond to varying wavelengths.

---

## Aim

To extract and analyze spectral responses of selected pixels from **Chandrayaan-2 IIRS hyperspectral data** and visualize their spectral curves using Python.

---

## Data Used

* **Chandrayaan-2 IIRS Hyperspectral Dataset**
* Format: **ENVI format**
* Files used:

  * `.hdr` → header file containing metadata
  * `.qub` → binary data cube containing spectral data

---

## Software and Libraries

The project uses the following tools and Python libraries:

* Python 3.x
* NumPy
* Matplotlib

Install required libraries using:

```bash
pip install numpy matplotlib
```

---

## Data Structure

The hyperspectral dataset is stored as a **3D data cube**:

```
(rows, columns, spectral bands)
```

Where:

* **Rows** → vertical spatial dimension
* **Columns** → horizontal spatial dimension
* **Bands** → spectral wavelength dimension

Each pixel contains a **spectral signature across multiple wavelengths**.

---

## Methodology

### 1. Read ENVI Header File

The `.hdr` file is read to extract important metadata such as:

* number of samples (columns)
* number of lines (rows)
* number of spectral bands
* data type
* wavelength information

---

### 2. Load Hyperspectral Data Cube

The `.qub` binary file is loaded into Python and converted into a **NumPy array**.

The data is reshaped into a **3D hyperspectral cube**:

```
cube = (rows, columns, bands)
```

---

### 3. Extract Wavelength Information

Wavelength values are obtained from the header file. These values correspond to the spectral bands recorded by the IIRS instrument.

If wavelength information is unavailable, band numbers are used instead.

---

### 4. Extract Pixel Spectral Values

Specific pixel locations are selected for analysis:

```
(50, 50)
(100, 100)
(150, 150)
```

For each pixel, radiance values across all spectral bands are extracted.

---

### 5. Plot Spectral Curves

The spectral values are plotted using **Matplotlib**, producing curves that represent:

```
X-axis → Wavelength
Y-axis → Radiance / Reflectance
```

Each pixel produces a unique spectral signature.

---

## Output

The script generates a **spectral curve plot** showing radiance variation across wavelengths for selected pixels.

<img width="1028" height="618" alt="image" src="https://github.com/user-attachments/assets/d7028595-e1b6-4629-b578-d2faa21c02a4" />
<p align="center">
 <em>Figure 1:Chandrayaan-2 IIRS Spectral Curve</em>
 </p>


The plot helps visualize:

* spectral patterns
* absorption features
* differences between surface materials

---

## Results

Spectral curves were successfully generated for multiple pixels from the IIRS hyperspectral dataset.

Observations include:

* Similar overall spectral trends among pixels
* Variation in radiance magnitude between pixels
* Distinct wavelength-dependent spectral responses

---

## Inference

* The selected pixels show **similar spectral patterns**, suggesting comparable surface material composition.
* **Higher radiance at shorter wavelengths** indicates strong reflectance typical of **lunar regolith or rocky terrain**.
* A **gradual decrease in radiance in mid-wavelengths** suggests possible **absorption features**, indicating material-specific spectral behavior.
* Radiance increases again at **longer wavelengths**, with slight variations among pixels, reflecting **spatial heterogeneity in lunar surface properties**.

---

## Applications

This workflow can be used for:

* lunar mineral detection
* spectral signature analysis
* hyperspectral remote sensing studies
* planetary surface characterization
* space mission data analysis

---

## Author

**Harshidha M**
PG Geoinformatics
