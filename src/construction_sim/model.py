from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from .config import SITE, SiteConfig


def load_schedule(path: str | Path) -> pd.DataFrame:
    schedule = pd.read_csv(path)
    required = {"stage", "name", "excavation_depth_m", "active_floor"}
    missing = required.difference(schedule.columns)
    if missing:
        raise ValueError(f"공정 데이터 필수 열 누락: {sorted(missing)}")
    return schedule.sort_values("stage").reset_index(drop=True)


def _box_trace(x0, x1, y0, y1, z0, z1, name, color, opacity=0.5):
    x = [x0, x1, x1, x0, x0, x1, x1, x0]
    y = [y0, y0, y1, y1, y0, y0, y1, y1]
    z = [z0, z0, z0, z0, z1, z1, z1, z1]
    i = [0, 0, 0, 1, 2, 4, 4, 5, 6, 4, 5, 6]
    j = [1, 2, 4, 2, 3, 5, 6, 6, 7, 7, 1, 2]
    k = [2, 3, 1, 5, 7, 6, 7, 2, 3, 0, 4, 7]
    return go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, name=name, color=color, opacity=opacity)


def build_figure(
    stage: int,
    visible: list[str],
    config: SiteConfig = SITE,
) -> go.Figure:
    fig = go.Figure()
    depth = min(stage * config.floor_height, config.basement_depth)

    if "cip" in visible and stage >= 1:
        wall = 0.65
        for args in [
            (0, config.width, 0, wall),
            (0, config.width, config.length - wall, config.length),
            (0, wall, 0, config.length),
            (config.width - wall, config.width, 0, config.length),
        ]:
            fig.add_trace(
                _box_trace(
                    *args, -config.basement_depth, 0, "CIP 흙막이", "#8b6f47", 0.42
                )
            )

    if "prd" in visible and stage >= 1:
        xs = [
            config.width * i / (config.prd_grid_x + 1)
            for i in range(1, config.prd_grid_x + 1)
        ]
        ys = [
            config.length * i / (config.prd_grid_y + 1)
            for i in range(1, config.prd_grid_y + 1)
        ]
        for x in xs:
            for y in ys:
                fig.add_trace(
                    go.Scatter3d(
                        x=[x, x],
                        y=[y, y],
                        z=[-config.basement_depth, 2],
                        mode="lines",
                        line={"color": "#40556b", "width": 5},
                        name="PRD 기둥",
                        showlegend=False,
                    )
                )

    if "slab" in visible:
        for floor in range(1, min(stage, 5) + 1):
            z = -(floor - 1) * config.floor_height
            fig.add_trace(
                _box_trace(
                    1,
                    config.width - 1,
                    1,
                    config.length - 1,
                    z - config.slab_thickness,
                    z,
                    f"슬래브 B{floor}",
                    "#aeb9c4",
                    0.32,
                )
            )

    if depth > 0:
        fig.add_trace(
            _box_trace(
                0.7,
                config.width - 0.7,
                0.7,
                config.length - 0.7,
                -depth,
                0,
                "굴착 영역",
                "#c9945b",
                0.12,
            )
        )

    fig.update_layout(
        scene={
            "xaxis_title": "폭 X (m)",
            "yaxis_title": "길이 Y (m)",
            "zaxis_title": "표고 Z (m)",
            "aspectmode": "data",
            "camera": {"eye": {"x": 1.5, "y": 1.6, "z": 1.1}},
        },
        margin={"l": 0, "r": 0, "t": 45, "b": 0},
        title=f"탑다운 공정 3D 개념 모델 — 단계 {stage}",
        legend={"orientation": "h"},
    )
    return fig
