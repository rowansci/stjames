from .base import Base
from typing import ClassVar


class Method(Base):
    name: str
    aliases: list[str] = []
    display_name: str
    corrections_allowed: bool = True
    basis_sets_allowed: bool = True

    _psi4_name: str | None = None
    _pyscf_name: str | None = None
    _terachem_name: str | None = None

    @property
    def psi4_name(self):
        return self._psi4_name if self._psi4_name is not None else self.name

    @property
    def pyscf_name(self):
        return self._pyscf_name if self._pyscf_name is not None else self.name

    @property
    def terachem_name(self):
        return self._terachem_name if self._terachem_name is not None else self.name


HARTREE_FOCK = Method(
    name="hf",
    display_name="HF",
)

HF3C = Method(
    name="hf_3c",
    display_name="HF-3c",
)

PBE = Method(
    name="pbe",
    display_name="PBE",
)

B973C = Method(
    name="b97_3c",
    aliases=["b973c", "b97-3c"],
    display_name="B97-3c",
    corrections_allowed=False,
    basis_sets_allowed=False,
)

R2SCAN = Method(
    name="r2scan",
    display_name="r2SCAN",
)

R2SCAN3C = Method(
    name="r2scan_3c",
    aliases=["r2scan3c", "r2scan-3c"],
    display_name="r2SCAN-3c",
    corrections_allowed=False,
    basis_sets_allowed=False,
)

TPSS = Method(
    name="tpss",
    display_name="TPSS",
)

M06L = Method(
    name="m06l",
    display_name="M06-L",
)

PBE0 = Method(
    name="pbe0",
    display_name="PBE0",
)

B3LYP = Method(
    name="b3lyp",
    display_name="B3LYP",
)

TPSSH = Method(
    name="tpssh",
    display_name="TPSSh",
)

M06 = Method(
    name="m06",
    display_name="M06",
)

M062X = Method(
    name="m062x",
    display_name="M06-2X",
)

CAMB3LYP = Method(
    name="camb3lyp",
    display_name="CAM-B3LYP",
)

WB97XD3 = Method(
    name="wb97x_d3",
    aliases=["wb97xd3", "wb97x-d3"],
    display_name="ωB97X-D3",
    corrections_allowed=False,
)

WB97XV = Method(
    name="wb97x_v",
    aliases=["wb97xv", "wb97x-v"],
    display_name="ωB97X-V",
    corrections_allowed=False,
)

WB97MV = Method(
    name="wb97m_v",
    aliases=["wb97mv", "wb97m-v"],
    display_name="ωB97M-V",
    corrections_allowed=False,
)

WB97MD3BJ = Method(
    name="wb97m_d3bj",
    aliases=["wb97md3bj", "wb97m-d3bj"],
    display_name="ωB97M-D3BJ",
    corrections_allowed=False,
)

WB97X3C = Method(
    name="wb97x_3c",
    aliases=["wb97x3c", "wb97x-3c"],
    display_name="ωB97X-3c",
    corrections_allowed=False,
    basis_sets_allowed=False,
)

DSDBLYPD3BJ = Method(
    name="dsd_blyp_d3bj",
    aliases=["dsdblypd3bj", "dsdblyp_d3bj", "dsd-blyp-d3bj"],
    display_name="DSD-BLYP-D3BJ",
    corrections_allowed=False,
)


AIMNET2_WB97MD3 = Method(
    name="aimnet2_wb97md3",
    display_name="AIMNet2 ωB97M-D3BJ",
    corrections_allowed=False,
    basis_sets_allowed=False,
)

GFN1_XTB = Method(
    name="gfn1_xtb",
    display_name="GFN1-xTB",
    corrections_allowed=False,
    basis_sets_allowed=False,
)

GFN2_XTB = Method(
    name="gfn2_xtb",
    display_name="GFN2-xTB",
    corrections_allowed=False,
    basis_sets_allowed=False,
)

GFN_FF = Method(
    name="gfnff",
    alises=["gfn_ff"],
    display_name="GFN-FF",
    corrections_allowed=False,
    basis_sets_allowed=False,
)
