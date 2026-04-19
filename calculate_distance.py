import math


def haversine(lat1, lon1, lat2, lon2):
    """Return distance in metres between two GPS coordinates."""
    R = 6_371_000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def total_distance(coords):
    """
    Calculate total distance from a list of (lat, lon) tuples.
    Returns distance in metres.
    """
    if len(coords) < 2:
        return 0.0
    return sum(
        haversine(coords[i - 1][0], coords[i - 1][1], coords[i][0], coords[i][1])
        for i in range(1, len(coords))
    )


if __name__ == "__main__":
    sample = [
        (53.3498, -6.2603),
        (53.3499, -6.2601),
        (53.3501, -6.2599),
        (53.3503, -6.2597),
        (53.3505, -6.2595),
        (53.3507, -6.2593),
    ]
    dist = total_distance(sample)
    print(f"Total distance covered: {dist:.1f} metres")
