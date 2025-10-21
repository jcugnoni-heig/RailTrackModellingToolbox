# Damper System Module

This module provides a Python class for modeling a two-mass damper system with coupling, including calculation of natural frequencies, stiffness, and damping vectors. It is designed for engineering applications such as vibration control and absorber design.

## Features
- Parameter validation for physical consistency
- Calculation of natural frequencies
- Computation of stiffness and damping vectors for each mass and the coupling
- Conversion to FEM units (N/mm, Ns/mm, Tonne)
- JSON serialization/deserialization for easy configuration management

## Dependencies
- numpy
- scipy

Install dependencies with:
```bash
pip install numpy scipy
```

## Main Class: `Damper`

### Constructor Parameters
- `M` (float): Total mass of the structure (kg)
- `f_target` (float): Target frequency (Hz)
- `m_total` (float): Total mass of absorbers (kg)
- `mass_ratio` (float): Mass distribution ratio (m1/m_total), between 0 and 1
- `coupling_coefficient` (float): Coupling coefficient for the coupling stiffness/damping
- `stiffness_vector_coef` (float): Coefficient for stiffness vectors (default: 0.3)
- `damping_vector_coef` (float): Coefficient for damping vectors (default: 0.3)
- `zeta` (float): Damping factor (default: 0.05)

### Main Methods
- `get_frequencies()`: Returns the natural frequencies (Hz)
- `get_stiffness_vectors_fem()`: Returns stiffness vectors (k1, k2, k3) in N/mm
- `get_damping_vectors_fem()`: Returns damping vectors (c1, c2, c3) in Ns/mm
- `get_masses_fem()`: Returns absorber masses (m1, m2) in Tonne
- `to_json(filepath=None)`: Serializes the configuration to JSON (and optionally saves to file)
- `from_json(json_str)`: Creates a Damper instance from a JSON string
- `from_json_file(filepath)`: Creates a Damper instance from a JSON file

### Example Usage
```python
from create_damper import Damper, InvalidParameterError

try:
    # Create a damper instance
    damper = Damper(
        M=36,                # Total mass (kg)
        f_target=1000,       # Target frequency (Hz)
        m_total=10,          # Total absorber mass (kg)
        mass_ratio=0.7,      # Mass ratio (m1/m_total)
        coupling_coefficient=0.8,  # Coupling coefficient
        stiffness_vector_coef=0.3,
        damping_vector_coef=0.3,
        zeta=0.08           # Damping factor
    )
    print(damper)
    print("\nNatural Frequencies:", damper.get_frequencies())
    k1, k2, k3 = damper.get_stiffness_vectors_fem()
    print("\nStiffness vector k1 (N/mm):", k1)

    # Save configuration to JSON
    damper.to_json("damper_config_optimized.json")
    print("\nConfiguration saved in 'damper_config_optimized.json'")

    # Load from JSON
    from_json = Damper.from_json_file("damper_config_optimized.json")
    print("\nLoaded from JSON:")
    print(from_json)

except InvalidParameterError as e:
    print(f"Parameter Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
```

### Running the Example
The script contains, at the end, an example of usage, you can thus directly run the script or change the values and run it with your desired properties:
```bash
python create_damper.py
```

This will display the damper system's properties, save the configuration to a JSON file, and demonstrate serialization/deserialization.
 