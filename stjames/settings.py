import pydantic
from typing import Optional, Any

from .modes import Mode
from .methods import Method
from .tasks import Task
from .base import Base
from .corrections import Correction
from .scf_settings import SCFSettings
from .basis_set import BasisSet
from .opt_settings import OptimizationSettings
from .thermochem_settings import ThermochemistrySettings


class Settings(Base):
    method: Method = Method.HARTREE_FOCK
    basis_set: BasisSet = BasisSet(name="STO-3G")
    tasks: list[Task] = [Task.ENERGY, Task.CHARGE, Task.DIPOLE]
    corrections: list[Correction] = []

    mode: Mode = Mode.AUTO

    # scf/opt settings will be set automatically based on mode, but can be overridden manually
    scf_settings: Optional[SCFSettings] = None
    opt_settings: Optional[OptimizationSettings] = None
    thermochem_settings: Optional[ThermochemistrySettings] = ThermochemistrySettings()

    @pydantic.computed_field
    @property
    def level_of_theory(self) -> str:
        if self.method in [Method.HF3C, Method.B973C]:
            return self.method.value
        elif (len(self.corrections)) == 0 or (self.method in [Method.B97D3]):
            return f"{self.method.value}/{self.basis_set.name.lower()}"
        else:
            return f"{self.method.value}-{'-'.join([c.value for c in self.corrections])}/{self.basis_set.name.lower()}"

    def model_post_init(self, __context: Any) -> None:
        _assign_settings_by_mode(self)

        # composite methods have their own basis sets, so overwrite user stuff
        if self.method == Method.HF3C:
            self.basis_set = BasisSet(name="minix")
        elif self.method == Method.B973C:
            self.basis_set = BasisSet(name="mTZVP")

    @pydantic.field_validator("basis_set", mode="before")
    @classmethod
    def inflate_basis_set(cls, v: Any) -> BasisSet:
        """Turn a string into a ``BasisSet`` object. (This is a little crude.)"""
        if isinstance(v, (BasisSet, dict)):
            return v
        elif isinstance(v, str):
            return BasisSet(name=v)
        elif v is None:
            return BasisSet(name="STO-3G")
        else:
            raise ValueError(f"invalid value ``{v}`` for ``basis_set``")


def _assign_settings_by_mode(settings: Settings) -> None:
    """Modifies ``scf_settings`` and ``opt_settings`` based on preset ``mode``."""
    mode = settings.mode

    if mode == Mode.AUTO:
        if (Task.OPTIMIZE in settings.tasks) or (Task.GRADIENT in settings.tasks) or (Task.FREQUENCIES) in settings.tasks or (Task.HESSIAN) in settings.tasks:
            mode = Mode.CAREFUL
        else:
            mode = Mode.RAPID

    if settings.scf_settings is None:
        scf_settings = SCFSettings()

        # values based off of the following sources:
        # qchem:
        #   https://manual.q-chem.com/5.2/Ch4.S3.SS2.html
        #   https://manual.q-chem.com/5.2/Ch4.S5.SS2.html
        #
        # gaussian:
        #   https://gaussian.com/integral/
        #   https://gaussian.com/overlay5/
        #
        # orca:
        #   manual 4.2.1, §9.6.1 and §9.7.3
        #
        # psi4:
        #   https://psicode.org/psi4manual/master/autodir_options_c/module__scf.html
        #   https://psicode.org/psi4manual/master/autodoc_glossary_options_c.html
        #
        # terachem:
        #   manual, it's easy to locate everything.
        #
        # the below values are my best attempt at homogenizing various sources.
        # in general, eri_threshold should be 3 OOM lower than scf convergence
        if mode == Mode.RECKLESS:
            scf_settings.energy_threshold = 1e-5
            scf_settings.rms_error_threshold = 1e-7
            scf_settings.max_error_threshold = 1e-4
            scf_settings.rebuild_frequency = 100
            scf_settings.int_settings.eri_threshold = 1e-8
            scf_settings.int_settings.csam_multiplier = 3.0
            scf_settings.int_settings.pair_overlap_threshold = 1e-9
            scf_settings.grid_settings.angular_num_points = 302
            scf_settings.grid_settings.radial_num_points = 75
        elif mode == Mode.RAPID:
            scf_settings.energy_threshold = 1e-6
            scf_settings.rms_error_threshold = 1e-8
            scf_settings.max_error_threshold = 1e-5
            scf_settings.rebuild_frequency = 20
            scf_settings.int_settings.eri_threshold = 1e-9
            scf_settings.int_settings.csam_multiplier = 1.0
            scf_settings.int_settings.pair_overlap_threshold = 1e-10
            scf_settings.grid_settings.angular_num_points = 590
            scf_settings.grid_settings.radial_num_points = 99
        elif mode == Mode.CAREFUL:
            scf_settings.energy_threshold = 1e-7
            scf_settings.rms_error_threshold = 1e-9
            scf_settings.max_error_threshold = 1e-6
            scf_settings.rebuild_frequency = 10
            scf_settings.int_settings.eri_threshold = 1e-10
            scf_settings.int_settings.csam_multiplier = 1.0
            scf_settings.int_settings.pair_overlap_threshold = 1e-10
            scf_settings.grid_settings.angular_num_points = 590
            scf_settings.grid_settings.radial_num_points = 99
        elif mode == Mode.METICULOUS:
            scf_settings.energy_threshold = 1e-8
            scf_settings.rms_error_threshold = 1e-9
            scf_settings.max_error_threshold = 1e-7
            scf_settings.rebuild_frequency = 5
            scf_settings.int_settings.eri_threshold = 1e-12
            scf_settings.int_settings.csam_multiplier = 1.0
            scf_settings.int_settings.pair_overlap_threshold = 1e-12
            scf_settings.grid_settings.angular_num_points = 770
            scf_settings.grid_settings.radial_num_points = 175
        elif mode == Mode.DEBUG:
            scf_settings.energy_threshold = 1e-9
            scf_settings.rms_error_threshold = 1e-10
            scf_settings.max_error_threshold = 1e-9
            scf_settings.rebuild_frequency = 1
            scf_settings.int_settings.eri_threshold = 1e-14
            scf_settings.int_settings.csam_multiplier = (
                1e10  # in other words, disable CSAM
            )
            scf_settings.int_settings.pair_overlap_threshold = 1e-14
            scf_settings.grid_settings.angular_num_points = 974
            scf_settings.grid_settings.radial_num_points = 250
        else:
            raise ValueError(f"Unknown mode ``{mode.value}``!")

        settings.scf_settings = scf_settings

    if settings.opt_settings is None:
        opt_settings = OptimizationSettings()

        # cf. DLFIND manual, and https://www.cup.uni-muenchen.de/ch/compchem/geom/basic.html
        if mode == Mode.RECKLESS:
            opt_settings.energy_threshold = 1e-5
            opt_settings.max_gradient_threshold = 4.5e-3
            opt_settings.rms_gradient_threshold = 3e-3
        elif mode == Mode.RAPID:
            opt_settings.energy_threshold = 1e-6
            opt_settings.max_gradient_threshold = 4.5e-4
            opt_settings.rms_gradient_threshold = 3e-4
        elif mode == Mode.CAREFUL:
            opt_settings.energy_threshold = 1e-6
            opt_settings.max_gradient_threshold = 4.5e-4
            opt_settings.rms_gradient_threshold = 3e-4
        elif mode == Mode.METICULOUS:
            opt_settings.energy_threshold = 1e-7
            opt_settings.max_gradient_threshold = 4.5e-5
            opt_settings.rms_gradient_threshold = 3e-5
        elif mode == Mode.DEBUG:
            opt_settings.energy_threshold = 1e-8
            opt_settings.max_gradient_threshold = 4.5e-6
            opt_settings.rms_gradient_threshold = 3e-6
        else:
            raise ValueError(f"Unknown mode ``{mode.value}``!")

        settings.opt_settings = opt_settings
