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
            (37.087787, 127.0571805),
            (37.089396, 127.0562793),
            (37.0902518, 127.056408),
            (37.091741, 127.055893),
            (37.0887627, 127.0446707),
            (37.0827544, 127.0446063),
            (37.0827202, 127.0462371),
            (37.0817958, 127.049048),
            (37.0775675, 127.0492411),
            (37.0750509, 127.0435119),
            (37.0756501, 127.0439411),
            (37.0767628, 127.043469),
            (37.0779612, 127.0425463),
            (37.0771566, 127.0407654),
            (37.0767457, 127.0406581),
            (37.0740579, 127.0410014),
            (37.074075, 127.0421172),
            (37.0701887, 127.0492841),
            (37.070103, 127.0543695),
            (37.0723972, 127.0544983),
            (37.0746913, 127.0543052),
            (37.0778585, 127.0540262),
            (37.0800668, 127.0540691),
            (37.0836446, 127.0553351),
            (37.087787, 127.0571805),
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
