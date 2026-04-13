import math

# 10 points, 1 second apart, simulating a player accelerating to a sprint
data = [
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

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

print(f"{'Time (s)':<12} {'Speed (km/h)':<15} {'Zone'}")
print("-" * 40)

max_speed = 0
total_distance = 0
sprint_distance = 0
high_intensity_distance = 0
sprint_count = 0
in_sprint = False

for i in range(1, len(data)):
    t1, lat1, lon1 = data[i-1]
    t2, lat2, lon2 = data[i]

    distance = haversine(lat1, lon1, lat2, lon2)
    time_diff = t2 - t1
    speed_ms = distance / time_diff
    speed_kmh = speed_ms * 3.6

    total_distance += distance

    if speed_kmh > max_speed:
        max_speed = speed_kmh

    if speed_kmh >= 20:
        high_intensity_distance += distance
    if speed_kmh >= 25:
        sprint_distance += distance

    # Sprint counting — only count a new sprint when we enter sprint zone
    if speed_kmh >= 25 and not in_sprint:
        sprint_count += 1
        in_sprint = True
    elif speed_kmh < 25:
        in_sprint = False

    if speed_kmh < 8:
        zone = "Walking"
    elif speed_kmh < 15:
        zone = "Jogging"
    elif speed_kmh < 20:
        zone = "Running"
    else:
        zone = "SPRINT"

    print(f"{t2:<12} {speed_kmh:<15.1f} {zone}")

print("-" * 40)
print(f"Max speed:                {max_speed:.1f} km/h")
print(f"Total distance:           {total_distance:.1f} m")
print(f"High intensity distance:  {high_intensity_distance:.1f} m")
print(f"Sprint distance:          {sprint_distance:.1f} m")
print(f"Sprint count:             {sprint_count}")