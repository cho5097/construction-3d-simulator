from construction_sim.model import build_figure, load_schedule


def test_load_schedule():
    schedule = load_schedule("data/schedule.csv")
    assert len(schedule) == 7
    assert schedule.iloc[-1]["active_floor"] == "MAT"


def test_stage_zero_has_excavation_only_when_depth_exists():
    figure = build_figure(0, ["cip", "prd", "slab"])
    assert len(figure.data) == 0


def test_stage_one_contains_cip_and_prd():
    figure = build_figure(1, ["cip", "prd"])
    assert len(figure.data) > 4

