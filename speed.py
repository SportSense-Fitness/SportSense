from calculate_distance import haversine

ZONES = [
    (0,   8,   "Walking"),
    (8,   15,  "Jogging"),
    (15,  20,  "Running"),
    (20,  999, "Sprint"),
]

SPRINT_THRESHOLD_KMH = 25
HI_THRESHOLD_KMH     = 20


def classify_zone(speed_kmh):
    for low, high, name in ZONES:
        if low <= speed_kmh < high:
            return name
    return "Sprint"


def analyse_session(data):
    """
    Analyse a GPS session.

    Args:
        data: list of (timestamp_s, lat, lon) tuples

    Returns:
        dict with keys: speeds, zones, total_distance_m, max_speed_kmh,
                        hi_distance_m, sprint_distance_m, sprint_count
    """
    speeds, zones = [], []
    total_dist = hi_dist = sprint_dist = 0.0
    sprint_count = 0
    in_sprint = False

    for i in range(1, len(data)):
        t1, lat1, lon1 = data[i - 1]
        t2, lat2, lon2 = data[i]

        dist_m   = haversine(lat1, lon1, lat2, lon2)
        dt       = t2 - t1 or 1          # guard against zero division
        speed_ms = dist_m / dt
        speed_kmh = speed_ms * 3.6

        total_dist += dist_m

        if speed_kmh >= HI_THRESHOLD_KMH:
            hi_dist += dist_m
        if speed_kmh >= SPRINT_THRESHOLD_KMH:
            sprint_dist += dist_m

        if speed_kmh >= SPRINT_THRESHOLD_KMH and not in_sprint:
            sprint_count += 1
            in_sprint = True
        elif speed_kmh < SPRINT_THRESHOLD_KMH:
            in_sprint = False

        speeds.append(round(speed_kmh, 1))
        zones.append(classify_zone(speed_kmh))

    return {
        "speeds":           speeds,
        "zones":            zones,
        "total_distance_m": round(total_dist, 1),
        "max_speed_kmh":    round(max(speeds, default=0), 1),
        "hi_distance_m":    round(hi_dist, 1),
        "sprint_distance_m": round(sprint_dist, 1),
        "sprint_count":     sprint_count,
    }


if __name__ == "__main__":
    sample = [
        (0,  53.34980, -6.26030),
        (1,  53.34982, -6.26028),
        (2,  53.34985, -6.26025),
        (3,  53.34989, -6.26021),
        (4,  53.34994, -6.26016),
        (5,  53.35000, -6.26010),
        (6,  53.35006, -6.26004),
        (7,  53.35012, -6.25998),
        (8,  53.35017, -6.25993),
        (9,  53.35021, -6.25989),
    ]

    result = analyse_session(sample)

    print(f"{'Time (s)':<10} {'Speed (km/h)':<15} {'Zone'}")
    print("-" * 38)
    for i, (spd, zone) in enumerate(zip(result["speeds"], result["zones"]), start=1):
        print(f"{i:<10} {spd:<15} {zone}")
    print("-" * 38)
    print(f"Max speed:         {result['max_speed_kmh']} km/h")
    print(f"Total distance:    {result['total_distance_m']} m")
    print(f"HI distance:       {result['hi_distance_m']} m")
    print(f"Sprint distance:   {result['sprint_distance_m']} m")
    print(f"Sprint count:      {result['sprint_count']}")
