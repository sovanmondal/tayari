"""Unit tests for impact aggregation (pure, no geospatial deps)."""
from app.domain.impact_model import estimate_impact
from app.domain.models import AdminUnit

MARSABIT = AdminUnit(id="KE-MBT", name="Marsabit", country="Kenya", level=1)


def test_triggered_exposes_full_population_split_by_livelihood():
    est = estimate_impact(
        MARSABIT,
        total_population=459_785,
        livelihood_shares={"pastoralist": 0.8, "farmer": 0.15, "urban": 0.05},
        triggered=True,
    )
    assert est.total_population_exposed == 459_785
    # Livelihood counts must sum exactly to the exposed total (rounding absorbed).
    assert sum(b.population for b in est.by_livelihood) == 459_785
    pastoral = next(b for b in est.by_livelihood if b.livelihood == "pastoralist")
    assert pastoral.population > 0


def test_not_triggered_zero_exposed():
    est = estimate_impact(
        MARSABIT,
        total_population=459_785,
        livelihood_shares={"pastoralist": 0.8, "farmer": 0.2},
        triggered=False,
    )
    assert est.total_population_exposed == 0
    assert est.by_livelihood == []


def test_method_is_documented():
    est = estimate_impact(MARSABIT, 1000, {"pastoralist": 1.0}, triggered=True)
    assert "CDI >= trigger" in est.method
