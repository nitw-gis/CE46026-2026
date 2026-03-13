# -------------------------------------------------------------
# Spectral Reflectance Simulation for Chandrayaan-2 IIRS Data
# This script demonstrates how radiance values can be converted
# into reflectance and visualized as a spectral curve.
# -------------------------------------------------------------

# 1. Import required scientific libraries
import numpy as np                     # Used for numerical calculations and array operations
import matplotlib.pyplot as plt        # Used for plotting graphs and visualization

# This Jupyter Notebook magic command ensures that plots
# are displayed inside the notebook instead of a separate window
%matplotlib inline


# -------------------------------------------------------------
# 2. Define function to convert radiance to reflectance
# -------------------------------------------------------------
def calculate_iirs_reflectance(radiance_data, solar_zenith_angle, esun_values, sun_distance_au=1.0):
    """
    Converts spectral radiance into reflectance.

    Reflectance Formula:
    Reflectance = (π * Radiance * d²) / (ESUN * cos(θ))

    Where:
    Radiance            = Sensor measured radiance
    ESUN                = Solar irradiance at the top of atmosphere
    θ (theta)           = Solar zenith angle
    d                   = Sun–target distance (in astronomical units)
    """

    # Convert solar zenith angle from degrees to radians
    theta_rad = np.radians(solar_zenith_angle)

    # Calculate denominator part of the reflectance equation
    denominator = esun_values * np.cos(theta_rad)

    # Apply reflectance formula
    reflectance = (np.pi * radiance_data * (sun_distance_au**2)) / denominator

    # Clip values between 0 and 1 since reflectance cannot exceed this range
    return np.clip(reflectance, 0, 1)


# -------------------------------------------------------------
# 3. Setup spectral range for IIRS sensor
# -------------------------------------------------------------

# IIRS (Imaging Infrared Spectrometer) measures wavelengths
# between 0.8 µm and 5.0 µm in the infrared region.
# Here we simulate 256 spectral bands across this range.
wavelengths = np.linspace(0.8, 5.0, 256)


# -------------------------------------------------------------
# 4. Simulate solar irradiance values (ESUN)
# -------------------------------------------------------------

# Solar irradiance decreases as wavelength increases
# in the infrared region. This equation approximates
# the spectral irradiance pattern.
esun_values = 1500 * (0.8 / wavelengths)**2


# -------------------------------------------------------------
# 5. Simulate lunar surface reflectance characteristics
# -------------------------------------------------------------

# Create a baseline reflectance trend (red spectral slope)
# Lunar soils usually show increasing reflectance with wavelength.
base_ref = 0.05 + 0.06 * (wavelengths - 0.8) / 4.2

# Simulate absorption features caused by minerals
# Gaussian curves represent mineral absorption bands
absorption_features = (
    0.02 * np.exp(-(wavelengths - 1.0)**2 / 0.02) +   # Pyroxene absorption near 1 µm
    0.03 * np.exp(-(wavelengths - 2.0)**2 / 0.05) +   # Pyroxene absorption near 2 µm
    0.09 * np.exp(-(wavelengths - 2.85)**2 / 0.12)    # OH/H2O absorption band
)

# Combine baseline reflectance and absorption dips
simulated_reflectance = np.clip(base_ref - absorption_features, 0.01, 1.0)


# -------------------------------------------------------------
# 6. Convert reflectance to radiance
# -------------------------------------------------------------

# Assume solar incidence angle (sun angle relative to surface)
incidence_angle = 30.0

# Convert reflectance back into radiance values
# This allows testing whether our reflectance calculation works
radiance_input = (
    simulated_reflectance * esun_values *
    np.cos(np.radians(incidence_angle))
) / np.pi


# -------------------------------------------------------------
# 7. Run reflectance calculation function
# -------------------------------------------------------------

final_reflectance = calculate_iirs_reflectance(
    radiance_input,
    incidence_angle,
    esun_values
)


# -------------------------------------------------------------
# 8. Plot the spectral reflectance curve
# -------------------------------------------------------------

plt.figure(figsize=(12, 6))

# Plot reflectance vs wavelength
plt.plot(
    wavelengths,
    final_reflectance,
    color='darkred',
    linewidth=2.5,
    label='IIRS Derived Reflectance'
)

# -------------------------------------------------------------
# 9. Annotate important mineral spectral features
# -------------------------------------------------------------

# Pyroxene absorption near 1 µm
plt.annotate(
    'Pyroxene (1µm)',
    xy=(1.0, 0.05),
    xytext=(0.9, 0.15),
    arrowprops=dict(arrowstyle='->')
)

# Pyroxene absorption near 2 µm
plt.annotate(
    'Pyroxene (2µm)',
    xy=(2.0, 0.06),
    xytext=(1.8, 0.18),
    arrowprops=dict(arrowstyle='->')
)

# Water / Hydroxyl absorption band
plt.annotate(
    'OH/H2O Band (2.8µm)',
    xy=(2.85, 0.04),
    xytext=(3.2, 0.05),
    arrowprops=dict(facecolor='black', shrink=0.05)
)

# -------------------------------------------------------------
# 10. Highlight hydration detection region
# -------------------------------------------------------------

plt.axvspan(
    2.7,
    3.1,
    color='skyblue',
    alpha=0.3,
    label='Hydration Detection Zone'
)

# -------------------------------------------------------------
# 11. Graph formatting
# -------------------------------------------------------------

plt.title('Spectral Reflectance Curve: IIRS Calibrated Data', fontsize=16)
plt.xlabel('Wavelength ($\mu$m)', fontsize=13)
plt.ylabel('Reflectance (0 to 1)', fontsize=13)

plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend(loc='upper left')

plt.xlim(0.8, 5.0)
plt.ylim(0, 0.3)

# Display the final plot
plt.show()

