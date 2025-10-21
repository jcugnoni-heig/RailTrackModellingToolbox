import numpy as np
from scipy.linalg import eig
import json
from typing import Dict, Any, Tuple

class DamperError(Exception):
    """Base class for Damper exceptions."""
    pass

class InvalidParameterError(DamperError):
    """Exception raised when a parameter is invalid."""
    pass

class Damper:
    def __init__(self, M: float, f_target: float, m_total: float, 
                 mass_ratio: float = 0.5, coupling_coefficient: float = 0.5, 
                 stiffness_vector_coef: float = 0.3, damping_vector_coef: float = 0.3, 
                 zeta: float = 0.05):
        """
        Initialize a damper system.
        
        Args:
            M (float): Total mass of the structure (kg)
            f_target (float): Target frequency (Hz)
            m_total (float): Total mass of absorbers (kg)
            mass_ratio (float): Mass distribution ratio (m1/m_total)
            coupling_coefficient (float): Coupling coefficient (for k2/c2)
            stiffness_vector_coef (float): Coefficient for stiffness vectors
            damping_vector_coef (float): Coefficient for damping vectors
            zeta (float): Damping factor
            
        Raises:
            InvalidParameterError: If a parameter is invalid
        """
        # Parameter validation
        self._validate_parameters(M, f_target, m_total, mass_ratio, 
                               coupling_coefficient, stiffness_vector_coef, damping_vector_coef, zeta)

        # Store initialization parameters
        self.M = M
        self.f_target = f_target
        self.m_total = m_total
        self.mass_ratio = mass_ratio
        self.coupling_coefficient = coupling_coefficient
        self.stiffness_vector_coef = stiffness_vector_coef
        self.damping_vector_coef = damping_vector_coef
        self.zeta = zeta

        # Derived calculations
        self.omega_target = 2 * np.pi * f_target
        self.m1 = m_total * mass_ratio
        self.m2 = m_total * (1 - mass_ratio)

        # Base stiffness calculations
        self.k1_base = (self.omega_target ** 2) * self.m1  # linked to m1
        self.k3_base = (self.omega_target ** 2) * self.m2  # linked to m2
        self.k2_base = coupling_coefficient * (self.k1_base + self.k3_base)  # coupling

        # Stiffness vectors
        self.k1 = np.array([stiffness_vector_coef * self.k1_base, self.k1_base, stiffness_vector_coef * self.k1_base])
        self.k3 = np.array([stiffness_vector_coef * self.k3_base, self.k3_base, stiffness_vector_coef * self.k3_base])
        self.k2 = np.array([stiffness_vector_coef * self.k2_base, self.k2_base, stiffness_vector_coef * self.k2_base])

        # Natural frequencies calculation
        K = np.array([[self.k1_base + self.k2_base, -self.k2_base], 
                     [-self.k2_base, self.k3_base + self.k2_base]])
        M_mat = np.array([[self.m1, 0], [0, self.m2]])
        eigvals, self.eigvecs = eig(K, M_mat)
        self.frequencies = np.sqrt(np.real(eigvals)) / (2 * np.pi)

        # Base damping calculations
        self.c1_base = 2 * zeta * np.sqrt(self.k1_base * self.m1)
        self.c3_base = 2 * zeta * np.sqrt(self.k3_base * self.m2)
        self.c2_base = 2 * zeta * np.sqrt(self.k2_base * (self.m1 + self.m2) / 2)

        # Damping vectors
        self.c1 = np.array([damping_vector_coef * self.c1_base, self.c1_base, damping_vector_coef * self.c1_base])
        self.c3 = np.array([damping_vector_coef * self.c3_base, self.c3_base, damping_vector_coef * self.c3_base])
        self.c2 = np.array([damping_vector_coef * self.c2_base, self.c2_base, damping_vector_coef * self.c2_base])

    def _validate_parameters(self, M: float, f_target: float, m_total: float,
                           mass_ratio: float, coupling_coefficient: float,
                           stiffness_vector_coef: float, damping_vector_coef: float,
                           zeta: float) -> None:
        """
        Validate input parameters.
        
        Args:
            M (float): Total mass of the structure
            f_target (float): Target frequency
            m_total (float): Total mass of absorbers
            mass_ratio (float): Mass distribution ratio
            coupling_coefficient (float): Coupling coefficient (for k2/c2)
            stiffness_vector_coef (float): Coefficient for stiffness vectors
            damping_vector_coef (float): Coefficient for damping vectors
            zeta (float): Damping factor
            
        Raises:
            InvalidParameterError: If a parameter is invalid
        """
        if M <= 0:
            raise InvalidParameterError(f"Total mass M must be positive, received: {M}")
        
        if f_target <= 0:
            raise InvalidParameterError(f"Target frequency must be positive, received: {f_target}")
        
        if m_total <= 0:
            raise InvalidParameterError(f"Total absorber mass must be positive, received: {m_total}")
        
        if not 0 < mass_ratio < 1:
            raise InvalidParameterError(f"Mass ratio must be between 0 and 1, received: {mass_ratio}")
        
        if coupling_coefficient <= 0:
            raise InvalidParameterError(f"Coupling coefficient must be positive, received: {coupling_coefficient}")
        
        if stiffness_vector_coef <= 0:
            raise InvalidParameterError(f"Stiffness vector coefficient must be positive, received: {stiffness_vector_coef}")
        
        if damping_vector_coef <= 0:
            raise InvalidParameterError(f"Damping vector coefficient must be positive, received: {damping_vector_coef}")
        
        if zeta <= 0:
            raise InvalidParameterError(f"Damping factor must be positive, received: {zeta}")

    def _convert_to_fem_units(self, value: float, unit_type: str) -> float:
        """
        Convert values to FEM units (N, mm, s, Tonne).
        
        Args:
            value (float): Value to convert
            unit_type (str): Type of unit ('mass', 'stiffness', 'damping')
            
        Returns:
            float: Converted value
        """
        if unit_type == 'mass':
            return value / 1000  # kg to Tonne
        elif unit_type == 'stiffness':
            return value / 1000  # N/m to N/mm
        elif unit_type == 'damping':
            return value / 1000  # Ns/m to Ns/mm
        return value

    def get_frequencies(self) -> np.ndarray:
        """Return the natural frequencies of the system in Hz."""
        return self.frequencies

    def get_stiffness_vectors_fem(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return the stiffness vectors k1 (m1), k2 (coupling), k3 (m2) in N/mm."""
        k1_fem = np.array([self._convert_to_fem_units(k, 'stiffness') for k in self.k1])
        k2_fem = np.array([self._convert_to_fem_units(k, 'stiffness') for k in self.k2])
        k3_fem = np.array([self._convert_to_fem_units(k, 'stiffness') for k in self.k3])
        return k1_fem, k2_fem, k3_fem

    def get_damping_vectors_fem(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return the damping vectors c1 (m1), c2 (coupling), c3 (m2) in Ns/mm."""
        c1_fem = np.array([self._convert_to_fem_units(c, 'damping') for c in self.c1])
        c2_fem = np.array([self._convert_to_fem_units(c, 'damping') for c in self.c2])
        c3_fem = np.array([self._convert_to_fem_units(c, 'damping') for c in self.c3])
        return c1_fem, c2_fem, c3_fem

    def get_masses_fem(self) -> Tuple[float, float]:
        """Return the masses m1 and m2 in Tonne."""
        m1_fem = self._convert_to_fem_units(self.m1, 'mass')
        m2_fem = self._convert_to_fem_units(self.m2, 'mass')
        return m1_fem, m2_fem

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the instance to a dictionary for JSON serialization.
        
        Returns:
            Dict[str, Any]: Dictionary containing the instance parameters
        """
        return {
            'M': float(self.M),
            'f_target': float(self.f_target),
            'm_total': float(self.m_total),
            'mass_ratio': float(self.mass_ratio),
            'coupling_coefficient': float(self.coupling_coefficient),
            'stiffness_vector_coef': float(self.stiffness_vector_coef),
            'damping_vector_coef': float(self.damping_vector_coef),
            'zeta': float(self.zeta)
        }

    def to_json(self, filepath: str = None) -> str:
        """
        Convert the instance to JSON.
        
        Args:
            filepath (str, optional): File path to save the JSON
            
        Returns:
            str: JSON representation of the instance
        """
        json_str = json.dumps(self.to_dict(), indent=4)
        if filepath:
            with open(filepath, 'w') as f:
                f.write(json_str)
        return json_str

    @classmethod
    def from_json(cls, json_str: str) -> 'Damper':
        """
        Create an instance from a JSON string.
        
        Args:
            json_str (str): JSON string containing the parameters
            
        Returns:
            Damper: New instance created from the JSON
        """
        params = json.loads(json_str)
        return cls(**params)

    @classmethod
    def from_json_file(cls, filepath: str) -> 'Damper':
        """
        Create an instance from a JSON file.
        
        Args:
            filepath (str): Path to the JSON file
            
        Returns:
            Damper: New instance created from the JSON file
        """
        with open(filepath, 'r') as f:
            params = json.load(f)
        return cls(**params)

    def __str__(self) -> str:
        """Text representation of the instance."""
        output = "Damper System:\n"
        output += "=" * 50 + "\n"
        
        # Initialization parameters
        output += "\nInitialization Parameters:\n"
        output += f"Total Mass (M): {self.M:.2f} kg\n"
        output += f"Target Frequency: {self.f_target:.0f} Hz\n"
        output += f"Total Absorber Mass: {self.m_total:.2f} kg\n"
        output += f"Mass Ratio: {self.mass_ratio:.2f}\n"
        output += f"Coupling Coefficient: {self.coupling_coefficient:.2f}\n"
        output += f"Stiffness Vector Coefficient: {self.stiffness_vector_coef:.2f}\n"
        output += f"Damping Vector Coefficient: {self.damping_vector_coef:.2f}\n"
        output += f"Damping Factor (zeta): {self.zeta:.2f}\n"
        
        # Calculated characteristics
        output += "\nCalculated Characteristics:\n"
        output += f"Mass m1: {self.m1:.2f} kg\n"
        output += f"Mass m2: {self.m2:.2f} kg\n"
        output += f"Natural Frequencies: {self.frequencies[0]:.0f} Hz, {self.frequencies[1]:.0f} Hz\n"
        
        # Stiffness vectors
        output += "\nStiffness Vectors (N/m):\n"
        output += f"k1 (m1): {self.k1}\n"
        output += f"k2 (coupling): {self.k2}\n"
        output += f"k3 (m2): {self.k3}\n"
        
        # Damping vectors
        output += "\nDamping Vectors (Ns/m):\n"
        output += f"c1 (m1): {self.c1}\n"
        output += f"c2 (coupling): {self.c2}\n"
        output += f"c3 (m2): {self.c3}\n"
        
        # FEM units
        output += "\nFEM Units:\n"
        m1_fem, m2_fem = self.get_masses_fem()
        output += f"Mass m1: {m1_fem:.3f} Tonne\n"
        output += f"Mass m2: {m2_fem:.3f} Tonne\n"
        
        k1_fem, k2_fem, k3_fem = self.get_stiffness_vectors_fem()
        output += f"\nStiffness Vectors (N/mm):\n"
        output += f"k1 (m1): {k1_fem}\n"
        output += f"k2 (coupling): {k2_fem}\n"
        output += f"k3 (m2): {k3_fem}\n"
        
        c1_fem, c2_fem, c3_fem = self.get_damping_vectors_fem()
        output += f"\nDamping Vectors (Ns/mm):\n"
        output += f"c1 (m1): {c1_fem}\n"
        output += f"c2 (coupling): {c2_fem}\n"
        output += f"c3 (m2): {c3_fem}\n"
        
        return output

# Usage example
if __name__ == "__main__":
    try:
        # Create an instance
        damper = Damper(
            M=60 * 0.6,  # Total mass
            f_target=1000,
            m_total=10,
            mass_ratio=0.7,  # Mass ratio
            coupling_coefficient=0.8,  # Coupling
            stiffness_vector_coef=0.3,
            damping_vector_coef=0.3,
            zeta=0.08  # Damping
        )
        
        # Display
        print(damper)
        
        # Example of method usage
        print("\nNatural Frequencies:", damper.get_frequencies())
        k1, k2, k3 = damper.get_stiffness_vectors_fem()
        print("\nVector k1 (N/mm):", k1)
        
        # Save configuration
        damper.to_json("damper_config_optimized.json")
        print("\nConfiguration saved in 'damper_config_optimized.json'")
        
        # Example of serialization/deserialization
        json_str = damper.to_json()
        print("\nJSON Representation:")
        print(json_str)
        
        # Create a new instance from JSON
        new_damper = Damper.from_json(json_str)
        print("\nNew Instance Created from JSON:")
        print(new_damper)
        
    except InvalidParameterError as e:
        print(f"Parameter Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
