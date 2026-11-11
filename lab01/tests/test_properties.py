import copy
from collections.abc import Sequence

from core import Parcel, process_parcels_pure
from hypothesis import given
from hypothesis import strategies as st

parcel_strategy = st.fixed_dictionaries(
    {
        "id": st.integers(min_value=1, max_value=10000),
        "weight": st.floats(
            min_value=0.1, max_value=49.9, allow_nan=False, allow_infinity=False
        ),
        "distance": st.floats(
            min_value=1.0, max_value=2000.0, allow_nan=False, allow_infinity=False
        ),
        "delivery_type": st.sampled_from(["standard", "express", "same_day"]),
        "paid": st.booleans(),
    }
)


@given(st.lists(parcel_strategy, min_size=0, max_size=25))
def test_property_referential_transparency(parcels: Sequence[Parcel]) -> None:
    report1 = process_parcels_pure(parcels, min_distance=10.0)
    report2 = process_parcels_pure(parcels, min_distance=10.0)
    assert report1 == report2


@given(st.lists(parcel_strategy, min_size=0, max_size=25))
def test_property_no_mutation(parcels: Sequence[Parcel]) -> None:
    snapshot = copy.deepcopy(list(parcels))
    _ = process_parcels_pure(parcels, min_distance=10.0)
    assert parcels == snapshot


@given(st.lists(parcel_strategy, min_size=0, max_size=25))
def test_property_invariants(parcels: Sequence[Parcel]) -> None:
    report = process_parcels_pure(parcels, min_distance=10.0)
    assert report["count"] == len(report["parcels"])
    assert report["total_cost"] >= 0.0
    for p in report["parcels"]:
        assert p["paid"] is True
        assert p["distance"] >= 10.0
        assert p.get("cost", 0.0) > 0.0
