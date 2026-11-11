import copy

from app import render_delivery_report
from core import (
    Parcel,
    calc_base_tariff,
    calc_delivery_cost,
    compose,
    linear_tariff_policy,
    make_delivery_processor,
    make_multiplier,
    pipe,
    process_parcels_pure,
    stamp_total,
    table_surcharge_policy,
)
from starter_imperative import process_parcels as imperative_process_parcels


def test_referential_transparency() -> None:
    res1 = calc_base_tariff(10.0, 50.0, per_kg=12.0, per_km=2.5)
    res2 = calc_base_tariff(10.0, 50.0, per_kg=12.0, per_km=2.5)
    assert res1 == res2 == (10.0 * 12.0 + 50.0 * 2.5)


def test_calc_delivery_cost_with_surcharge() -> None:
    tariff = linear_tariff_policy(10.0, 2.0)
    surcharge = table_surcharge_policy({"express": 1.5})
    cost = calc_delivery_cost(2.0, 40.0, "express", tariff, surcharge)
    assert cost == 150.0


def test_immutability_of_input_parcels(sample_parcels: list[Parcel]) -> None:
    parcels_before = copy.deepcopy(sample_parcels)
    report = process_parcels_pure(sample_parcels, min_distance=10.0)

    assert sample_parcels == parcels_before
    for p in report["parcels"]:
        original = next(x for x in sample_parcels if x["id"] == p["id"])
        assert "cost" not in original
        assert "cost" in p


def test_equivalence_with_imperative(sample_parcels: list[Parcel]) -> None:
    parcels_for_imp = copy.deepcopy(sample_parcels)
    imp_res = imperative_process_parcels(parcels_for_imp, min_distance=15.0)

    pure_res = process_parcels_pure(sample_parcels, min_distance=15.0)

    assert pure_res["count"] == imp_res["count"]
    assert pure_res["total_cost"] == imp_res["total_cost"]
    for p, imp_p in zip(pure_res["parcels"], imp_res["parcels"], strict=True):
        assert p["id"] == imp_p["id"]
        assert p["cost"] == imp_p["cost"]


def test_make_delivery_processor_custom_callable() -> None:
    custom_processor = make_delivery_processor(
        accept=lambda p: p["weight"] < 4.0,
        tariff_fn=lambda w, d: 50.0,
        surcharge_fn=lambda t: 2.0,
    )
    parcels: list[Parcel] = [
        {
            "id": 1,
            "weight": 2.0,
            "distance": 10.0,
            "delivery_type": "standard",
            "paid": True,
        },
        {
            "id": 2,
            "weight": 5.0,
            "distance": 10.0,
            "delivery_type": "standard",
            "paid": True,
        },
    ]
    report = custom_processor(parcels)
    assert report["count"] == 1
    assert report["parcels"][0]["id"] == 1
    assert report["parcels"][0]["cost"] == 100.0


def test_compose_and_pipe() -> None:
    def add_five(x: float) -> float:
        return x + 5.0

    def double(x: float) -> float:
        return x * 2.0

    fn = compose(double, add_five)
    assert fn(10.0) == 30.0

    assert pipe(10.0, add_five, double) == 30.0


def test_make_multiplier() -> None:
    m = make_multiplier(3.0)
    assert m(4.0) == 12.0


def test_stamp_total() -> None:
    fixed_time = 1700000000.0
    total, ts = stamp_total(lambda a, b: a + b, lambda: fixed_time, 15.0, 25.0)
    assert total == 40.0
    assert ts == fixed_time


def test_render_delivery_report(sample_parcels: list[Parcel]) -> None:
    report = process_parcels_pure(sample_parcels)
    text = render_delivery_report(report)
    assert "ЗВІТ СИСТЕМИ ДОСТАВКИ" in text
    assert str(report["count"]) in text
