from pathlib import Path

from dash import Dash, Input, Output, dcc, html

from .model import build_figure, load_schedule

ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_PATH = ROOT / "data" / "schedule.csv"
schedule = load_schedule(SCHEDULE_PATH)

app = Dash(__name__)
app.title = "공사 3D 시뮬레이터"
app.layout = html.Div(
    [
        html.H2("광주 농성동 탑다운 공사 3D 시뮬레이터"),
        html.P("공정 단계와 표시 항목을 선택하여 지하 시공 순서를 검토합니다."),
        dcc.Slider(
            id="stage",
            min=int(schedule.stage.min()),
            max=int(schedule.stage.max()),
            step=1,
            value=1,
            marks={int(r.stage): str(r.name) for r in schedule.itertuples()},
        ),
        dcc.Checklist(
            id="visible",
            options=[
                {"label": "CIP 흙막이", "value": "cip"},
                {"label": "PRD 기둥", "value": "prd"},
                {"label": "슬래브", "value": "slab"},
            ],
            value=["cip", "prd", "slab"],
            inline=True,
        ),
        html.Div(
            id="stage-summary",
            style={"margin": "12px 0", "fontWeight": "600"},
        ),
        dcc.Graph(id="model", style={"height": "72vh"}),
    ],
    style={
        "fontFamily": "Arial, sans-serif",
        "maxWidth": "1400px",
        "margin": "auto",
        "padding": "20px",
    },
)


@app.callback(
    Output("model", "figure"),
    Output("stage-summary", "children"),
    Input("stage", "value"),
    Input("visible", "value"),
)
def update(stage, visible):
    row = schedule.loc[schedule.stage == stage].iloc[0]
    summary = (
        f"{row['name']} | 굴착 깊이 {row['excavation_depth_m']}m | "
        f"예정 {row['duration_days']}일"
    )
    return build_figure(int(stage), visible or []), summary


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
