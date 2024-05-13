import math
from shapely.geometry import Point, Polygon


def get_coordinates_distance_km(coor1, coor2):
    x1, y1 = coor1
    x2, y2 = coor2

    radius = 6371  # 지구 반지름(km)
    to_radian = math.pi / 180

    delta_latitude = abs(x1 - x2) * to_radian
    delta_longitude = abs(y1 - y2) * to_radian

    sin_delta_lat = math.sin(delta_latitude / 2)
    sin_delta_lng = math.sin(delta_longitude / 2)
    square_root = math.sqrt(
        sin_delta_lat**2
        + math.cos(x1 * to_radian) * math.cos(x2 * to_radian) * sin_delta_lng**2
    )

    distance = 2 * radius * math.asin(square_root)

    return distance


def check_coordinate_in_polygon(coor):
    polygon = Polygon(
        [
            (37.0834426, 127.049503),
            (37.0813542, 127.049503),
            (37.0800874, 127.0498034),
            (37.0778277, 127.0498892),
            (37.0772114, 127.0493742),
            (37.0747119, 127.0494171),
            (37.0733423, 127.0498892),
            (37.0719727, 127.0499321),
            (37.0705688, 127.0488163),
            (37.0664254, 127.0532366),
            (37.079163, 127.0538803),
            (37.0803271, 127.0539662),
            (37.0812173, 127.0543524),
            (37.0833057, 127.0551678),
            (37.0833742, 127.053537),
            (37.0839904, 127.0529791),
            (37.0833399, 127.0518204),
            (37.0834426, 127.049503),
        ]
    )

    return polygon.contains(Point(coor))


import random

def test():
    for _ in range(10):
        # 랜덤한 좌표 생성
        coor = generate_random_coordinate()
        result = check_coordinate_in_polygon(coor)
        print(f"좌표 {coor}의 다각형 내부 포함 여부: {result}")
        
def generate_random_coordinate():
    # 37.06과 37.09 사이의 랜덤한 위도 생성
    latitude = random.uniform(37.06, 37.09)
    # 127.04와 127.06 사이의 랜덤한 경도 생성
    longitude = random.uniform(127.04, 127.06)
    return (latitude, longitude)
