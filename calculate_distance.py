import math

data = [
    (53.3498, -6.2603),
    (53.3499, -6.2601),
    (53.3501, -6.2599),
    (53.3503, -6.2597),
    (53.3505, -6.2595),
    (53.3507, -6.2593),
]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

total_distance = 0

for i in range(1, len(data)):
    lat1, lon1 = data[i-1]
    lat2, lon2 = data[i]
    total_distance += haversine(lat1, lon1, lat2, lon2)

print(f"Total distance covered: {total_distance:.1f} metres")