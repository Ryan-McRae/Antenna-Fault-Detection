## Explaining RF Features

### 1\. S11 (Return Loss, dB)

S11 measures how much of the electrical signal is reflected back toward the transmitter due to impedance mismatch. In an ideal system, energy is fully converted to radiated radio waves.

- **Target Behavior:** A healthy return loss is negative, typically between −10 dB−10 dB and −20 dB−20 dB, indicating minimal signal echo.

### 2\. VSWR (Voltage Standing Wave Ratio)

VSWR offers a complementary perspective to return loss. When a reflected wave meets an incoming wave, it creates a standing wave along the transmission line.

- **Target Behavior:** Lower VSWR values (approaching 1.01.0) indicate optimal power transfer. Excessively high standing waves can cause dangerous voltage spikes and transmitter damage.

### 3\. Gain (dBi)

Gain measures how effectively the antenna focuses radiated power in a specific direction relative to an isotropic radiator. High gain reflects concentrated directional efficiency.

### 4\. Efficiency (%)

Efficiency is the ratio of total radiated power to input power, accounting for ohmic losses, dielectric losses, and mismatch losses.

### 5\. Bandwidth (MHz)

Bandwidth defines the continuous frequency range over which the antenna maintains acceptable operating performance and matching characteristics.

### 6\. Input Impedance (ZZ)

Impedance represents the total electrical opposition the radio encounters when driving the antenna. It is split into two components:

- **ZRealZReal​ (Resistance):** The productive component representing energy actually radiated as radio waves (plus minimal conductor resistance). In standard systems, this should target 50 Ω50Ω to match transmission lines.
- **ZImagZImag​ (Reactance):** The reactive component representing energy temporarily stored in near-field electric or magnetic fields that bounces back instead of radiating. This should remain as close to 0 Ω0Ω as possible at the operating frequency.

## Mapping Physical Faults to RF Signatures

The core objective is to map these 7 RF features to 6 distinct physical states (encoded from 00 to 55):

- **0 -\> Healthy:** Nominal geometry, clean contacts, standard conditions.
- **1 -\> Broken Element:** Severed or fractured radiating element altering current paths.
- **2 -\> Length Variation:** Physical dimensional shift altering resonant frequency.
- **3 -\> Bad Connection:** Contact resistance from loose joints or corrosion.
- **4 -\> Bending:** Structural warping altering spatial geometry and mutual coupling.
- **5 -\> Humidity:** Moisture ingress introducing high dielectric loading.

## Physical-to-Electrical Expectations

- **Broken Element (1):** Catastrophically impacts return loss (S11) and VSWR, completely shifting resonant frequency and degrading Gain and Bandwidth.
- **Length Variation (2):** Shifts resonance away from the operating frequency, impacting impedance, bandwidth, S11, efficiency, and VSWR.
- **Bad Connection (3):** Introduces series resistance, directly hitting efficiency, gain, and real impedance (ZRealZReal​).
- **Bending (4):** Distorts current distribution and radiation patterns, primarily affecting Gain and reactive impedance (ZImagZImag​).
- **Humidity (5):** Water has a high relative permittivity (ϵr≈80ϵr​≈80), which increases electrical length, introduces heavy dielectric losses, and impacts efficiency, impedance, and bandwidth.

## Data Analysis & Results

To evaluate feature sensitivity, the average Z-score for each feature was calculated and grouped by fault type. Because the data is Z-scored globally, a value of 0 represents the dataset-wide average, while a value of ±1 indicates one standard deviation away.

### The "Healthy" Baseline Effect

An important nuance in the dataset is the representation of the Healthy state. Because the dataset is perfectly balanced across 6 conditions, Healthy makes up exactly 1/61/6 of the data.

Because the global mean is heavily weighted by the 5 faulty states (where efficiency drops, S11 spikes, and performance degrades), the global average (0.00.0) does not represent a "normal" antenna. Instead, optimal Healthy performance sits out on the positive tail of the distribution, while failure modes occupy the rest of the space.

### Feature-by-Feature Sensitivity Summary

- **S11:** Strongly sensitive to Length Variation (2) and Humidity (5).
- **VSWR:** Strongly responsive to Length Variation (2) and Humidity (5), with minor shifts during Broken Element (1) and Bending (4).
- **Gain:** Acts as a primary indicator for Length Variation (2) and Humidity (5).
- **Efficiency:** Heavily degraded by Length Variation (2) and Humidity (5).
- **Bandwidth:** Narrows noticeably under Length Variation (2) and Humidity (5).
- **ZImagZImag​ (Reactance):** Highly sensitive to Bad Connection (3), Bending (4), and Humidity (5).
- **ZRealZReal​ (Resistance):** Shifts visibly during Bad Connection (3) and Humidity (5).