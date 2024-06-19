from typing import Any, Optional

from ..base import Base
from ..constraint import Constraint
from ..method import Method
from ..mode import Mode
from ..solvent import Solvent
from .workflow import Workflow


class ConformerSettings(Base):
    num_confs_considered: int = 100
    num_confs_taken: int = 50
    rmsd_cutoff: float = 0.1

    final_method: Method = Method.AIMNET2_WB97MD3
    solvent: Optional[Solvent] = Solvent.WATER
    max_energy: float = 5

    constraints: list[Constraint] = []


class RdkitConformerSettings(ConformerSettings):
    num_initial_confs: int = 100
    max_mmff_energy: float = 10
    max_mmff_iterations: int = 500


class CrestConformerSettings(ConformerSettings):
    flags: str = "--quick --ewin 10"
    gfn: int | str = "ff"


class Conformer(Base):
    energy: float
    weight: Optional[float] = None

    # uuid, optionally
    uuid: Optional[str] = None


class ConformerWorkflow(Workflow):
    mode: Mode = Mode.RAPID
    settings: ConformerSettings = ConformerSettings()
    conformers: list[Conformer] = []

    def model_post_init(self, __context: Any) -> None:
        self.settings = csearch_settings_by_mode(self.mode)


def csearch_settings_by_mode(mode: Mode) -> ConformerSettings:
    if mode == Mode.METICULOUS:
        return CrestConformerSettings(
            gfn=2,
            flags="--ewin 15",
            max_energy=10,
            num_confs_considered=500,
            num_confs_taken=150,
        )

    elif mode == Mode.CAREFUL:
        return CrestConformerSettings(
            gfn="ff",
            flags="--quick --ewin 10",
            num_confs_considered=150,
            num_confs_taken=50,
        )

    elif mode == Mode.RAPID or Mode.AUTO:
        return RdkitConformerSettings(
            num_initial_confs=300,
            max_mmff_energy=15,
            num_confs_considered=100,
            num_confs_taken=50,
        )

    elif mode == Mode.RECKLESS:
        return RdkitConformerSettings(
            num_initial_confs=200,
            max_mmff_energy=10,
            num_confs_considered=50,
            num_confs_taken=20,
            rmsd_cutoff=0.25,
        )

    else:
        raise ValueError(f"invalid mode ``{mode.value}`` for conformer settings")
