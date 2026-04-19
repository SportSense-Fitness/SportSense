"""
SportSense — unit tests
Run with:  python test.py
"""
from calculate_distance import haversine, total_distance
from speed import analyse_session, classify_zone


def ok(label):
    print(f"  PASS  {label}")

def fail(label, got, expected):
    print(f"  FAIL  {label} — got {got}, expected {expected}")


def test_haversine():
    # Known distance: Dublin city centre → approx 111 m per 0.001° lat
    d = haversine(53.3498, -6.2603, 53.3508, -6.2603)
    assert 100 < d < 120, f"haversine sanity check failed: {d}"
    ok("haversine returns sensible distance")

def test_total_distance():
    coords = [
        (53.3498, -6.2603),
        (53.3499, -6.2601),
        (53.3501, -6.2599),
    ]
    d = total_distance(coords)
    assert d > 0, "total_distance should be positive"
    ok("total_distance sums correctly")

    assert total_distance([]) == 0.0
    ok("total_distance handles empty list")

    assert total_distance([(53.3498, -6.2603)]) == 0.0
    ok("total_distance handles single point")

def test_classify_zone():
    assert classify_zone(5)  == "Walking"
    assert classify_zone(10) == "Jogging"
    assert classify_zone(17) == "Running"
    assert classify_zone(28) == "Sprint"
    ok("classify_zone returns correct zones")

def test_analyse_session():
    data = [
        (0,  53.34980, -6.26030),
        (1,  53.34982, -6.26028),
        (2,  53.34985, -6.26025),
        (3,  53.34989, -6.26021),
        (4,  53.34994, -6.26016),
        (5,  53.35000, -6.26010),
    ]
    r = analyse_session(data)
    assert r["total_distance_m"] > 0,   "should have positive distance"
    assert r["max_speed_kmh"]    > 0,   "should have positive max speed"
    assert r["sprint_count"]    >= 0,   "sprint count should be non-negative"
    assert len(r["speeds"]) == len(data) - 1
    ok("analyse_session returns complete result dict")

    # Edge case: only one point — no intervals possible
    r2 = analyse_session([(0, 53.0, -6.0)])
    assert r2["total_distance_m"] == 0.0
    ok("analyse_session handles single-point session")


if __name__ == "__main__":
    print("\nSportSense test suite")
    print("=" * 40)
    tests = [
        test_haversine,
        test_total_distance,
        test_classify_zone,
        test_analyse_session,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"  ERROR in {t.__name__}: {e}")
    print("=" * 40)
    print(f"{passed}/{len(tests)} test groups passed\n")
