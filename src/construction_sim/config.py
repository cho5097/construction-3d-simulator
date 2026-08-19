from dataclasses import dataclass


@dataclass(frozen=True)
class SiteConfig:
    """개념 모델의 현장 형상 및 주요 치수(단위: m)."""

    width: float = 70.0
    length: float = 95.0
    basement_depth: float = 20.0
    floor_height: float = 4.0
    cip_spacing: float = 0.63
    prd_grid_x: int = 5
    prd_grid_y: int = 7
    slab_thickness: float = 0.35


SITE = SiteConfig()

