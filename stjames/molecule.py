import pydantic
from typing import Optional

from .base import Base


class VibrationalMode(Base):
    frequency: float
    reduced_mass: float
    force_constant: float
    displacements: list[list[float]]


class Atom(Base):
    atomic_number: pydantic.NonNegativeInt
    position: list[float]


class Molecule(Base):
    charge: int
    multiplicity: pydantic.PositiveInt
    atoms: list[Atom]

    energy: Optional[float] = None
    scf_iterations: Optional[pydantic.NonNegativeInt] = None
    scf_completed: Optional[bool] = None
    elapsed: Optional[float] = None

    gradient: Optional[list[list[float]]] = None
    density_matrix: Optional[list[list[float]]] = None
    hessian: Optional[list[list[list[list[float]]]]] = None

    atomic_charges: Optional[list[float]] = None
    atomic_spin_densities: Optional[list[float]] = None
    dipole: Optional[list[float]] = None

    vibrational_modes: Optional[list[VibrationalMode]] = None

    zero_point_energy: Optional[float] = None
    thermal_energy_corr: Optional[float] = None
    thermal_enthalpy_corr: Optional[float] = None
    thermal_free_energy_corr: Optional[float] = None

    @property
    def coordinates(self):
        return [a.position for a in self.atoms]

    @property
    def atomic_numbers(self):
        return [a.atomic_number for a in self.atoms]

    @property
    def sum_energy_zpe(self) -> float | None:
        if (self.energy is None) or (self.zero_point_energy is None):
            return None
        else:
            return self.energy + self.zero_point_energy

    @property
    def sum_energy_thermal_corr(self) -> float | None:
        if (self.energy is None) or (self.thermal_energy_corr is None):
            return None
        else:
            return self.energy + self.thermal_energy_corr

    @property
    def sum_energy_enthalpy(self) -> float | None:
        if (self.energy is None) or (self.thermal_enthalpy_corr is None):
            return None
        else:
            return self.energy + self.thermal_enthalpy_corr

    @property
    def sum_energy_free_energy(self) -> float | None:
        if (self.energy is None) or (self.thermal_free_energy_corr is None):
            return None
        else:
            return self.energy + self.thermal_free_energy_corr
