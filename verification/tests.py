from math import sqrt
from itertools import combinations
from collections import defaultdict
from random import choice


def judge(room, sensors):
    corners = (0, 0), (0, room[1]), (room[0], 0), (room[0], room[1])
    uncovered_dots = defaultdict(int)
    [uncovered_dots.update({d: 0}) for d in corners]

    if len(sensors) == 1: return all([is_in_range(d, sensors[0]) for d in uncovered_dots])

    for s1, s2 in combinations(sensors, 2):
        dots = sensors_intersections(s1, s2)
        if dots:
            for x, y in dots:
                if 0 <= x <= room[0] and 0 <= y <= room[1]: uncovered_dots[(x, y)] = 0

    for sensor in sensors:
        intersections = borders_intersections(room, sensor)
        for dot in intersections:
            uncovered_dots[dot] = 0

    for sensor in sensors:
        for dot in uncovered_dots:
            uncovered_dots[dot] += 1 if is_in_range(dot, sensor) else 0

    [print(k, v) for k, v in uncovered_dots.items()]
    for (x, y), n in uncovered_dots.items():
        if n < 1: return False
        if n == 1 and (x, y) not in corners: return False
        if n == 2 and 0 < x < room[0] and 0 < y < room[1]: return False
    return True


def is_in_range(dot, sensor):
    x, y, r = sensor
    x0, y0 = dot
    return sqrt((x-x0)**2 + (y-y0)**2) < r + 10e-6


def borders_intersections(room, sensor):
    dots = []
    xr, yr = room
    x, y, r = sensor
    if x <= r:
        dy = round(sqrt(r**2 - x**2),6)
        if y + dy <= yr: dots.append((0, y+dy))
        if y - dy >= 0: dots.append((0, y-dy))
    if x + r >= xr:
        dy = round(sqrt(r**2 - (xr-x)**2), 6)
        if y + dy <= yr: dots.append((xr, y+dy))
        if y - dy >= 0: dots.append((xr, y-dy))
    if y <= r:
        dx = round(sqrt(r**2 - y**2), 6)
        if x + dx <= xr: dots.append((x+dx, 0))
        if x - dx >= 0: dots.append((x-dx, 0))
    if y + r >= yr:
        dx = round(sqrt(r**2 - (yr-y)**2), 6)
        if x + dx <= xr: dots.append((x+dx, yr))
        if x - dx >= 0: dots.append((x-dx, yr))
    return dots


def sensors_intersections(sensor1, sensor2):
    dots = []
    x1, y1, r1 = sensor1
    x2, y2, r2 = sensor2
    d = round(sqrt((x2-x1)**2 + (y2-y1)**2), 6)
    if r1 + r2 >= d > abs(r1-r2):

        a = (r1**2 - r2**2 + d**2)/(2*d)
        h = sqrt(r1**2 - a**2)

        x_d = x1 + a*(x2 - x1)/d
        y_d = y1 + a*(y2 - y1)/d

        x_int_1 = round(x_d + h*(y2 - y1)/d, 6)
        y_int_1 = round(y_d - h*(x2 - x1)/d, 6)

        x_int_2 = round(x_d - h*(y2 - y1)/d, 6)
        y_int_2 = round(y_d + h*(x2 - x1)/d, 6)

        dots.extend([(x_int_1, y_int_1), (x_int_2, y_int_2)])
    return dots


def make_random_test_test(n):
    tests = []
    for _ in range(n):
        h = choice(range(100, 1100, 50))
        w = h * choice(range(1, 5))
        x_interval = list(range(0, w+5, w//20))
        y_interval = list(range(0, h+5, h//20))
        r_interval = list(range(h//10, h, h//20))
        sensors_num = choice(range(5, 11))
        sensors = []
        for _ in range(sensors_num):
            x = choice(x_interval)
            x_interval.remove(x)
            y = choice(y_interval)
            y_interval.remove(y)
            r = choice(r_interval)
            r_interval.remove(r)
            sensors.append([x, y, r])
        tests.append(
            {
                "input": [[w, h], sensors],
                "answer": judge([w, h], sensors)
            }
        )
    return tests


TESTS = {
    "Basics": [
        {
            "input": [[200, 150], [[100, 75, 130]]],
            "answer": True
        },
        {
            "input": [[200, 150], [[50, 75, 100], [150, 75, 100]]],
            "answer": True
        },
        {
            "input": [[200, 150], [[50, 75, 100], [150, 25, 50], [150, 125, 50]]],
            "answer": False,
        },
        {
            "input": [[200, 150], [[100, 75, 100], [0, 40, 60], [0, 110, 60], [200, 40, 60], [200, 110, 60]]],
            "answer": True
        },
        {
            "input": [[200, 150], [[100, 75, 100], [0, 40, 50], [0, 110, 50], [200, 40, 50], [200, 110, 50]]],
            "answer": False
        },
        {
            "input": [[200, 150], [[100, 75, 110], [105, 75, 110]]],
            "answer": False
        },
        {
            "input": [[200, 150], [[100, 75, 110], [105, 75, 20]]],
            "answer": False
        },
        {
            "input": [[3, 1], [[1, 0, 2], [2, 1, 2]]],
            "answer": True
        },
        {
            "input": [[30, 10], [[0, 10, 10], [10, 0, 10], [20, 10, 10], [30, 0, 10]]],
            "answer": True
        },
        {
            "input": [[30, 10], [[0, 10, 8], [10, 0, 7], [20, 10, 9], [30, 0, 10]]],
            "answer": False
        }
    ],
    "Extra": [
        {
            "input": [[8, 6], [[4, 3, 5]]],
            "answer": True
        },
        {
            "input": [[2000, 1000], [[0, 0, 500], [500, 0, 500], [1000, 0, 500], [1500, 0, 500],
                                     [2000, 0, 500], [0, 500, 500], [500, 500, 500], [1000, 500, 500],
                                     [1500, 500, 500], [2000, 500, 500]]],
            "answer": False
        },
        {
            "input": [[4000, 1000], [[0, 500, 1600], [2000, 100, 500], [2100, 900, 500],
                                     [2500, 200, 500], [2600, 800, 500], [4000, 0, 1200]]],
            "answer": False
        },
        {
            "input": [[4000, 1000], [[0, 500, 1600], [2000, 100, 500], [2100, 900, 500],
                                     [2500, 200, 500], [2600, 800, 500], [4000, 0, 1200], [4000, 500, 200]]],
            "answer": False
        },
        {
            "input": [[4000, 1000], [[0, 500, 1600], [2000, 100, 500], [2100, 900, 500],
                                     [2500, 200, 500], [2600, 800, 500], [4000, 500, 1200], [1600, 500, 600]]],
            "answer": True
        },
        {
            "input": [[4000, 1000], [[0, 500, 1600], [2000, 100, 500], [2100, 900, 500],
                                     [2500, 200, 500], [2600, 800, 500], [4000, 600, 1200], [1600, 500, 600]]],
            "answer": False
        },
        {
            "input": [[100, 100], [[50, 50, 65], [25, 25, 25], [25, 75, 25], [75, 25, 25], [75, 75, 25]]],
            "answer": False
        },
        {
            "input": [[100, 100], [[50, 50, 65], [5, 5, 25], [5, 95, 25], [95, 5, 25], [95, 95, 25]]],
            "answer": True
        },
        {
            "input": [[800, 800], [[0, 0, 500], [0, 800, 500], [800, 0, 500], [800, 800, 500]]],
            "answer": False
        },
        {
            "input": [[800, 800], [[0, 0, 570], [0, 800, 500], [800, 0, 500], [800, 800, 570]]],
            "answer": True
        },
        {
            "input": [[300, 150], [[40, 60, 240], [240, 140, 100], [295, 10, 50]]]],
            "answer": False
        }        
        
    ],
    "Randoms": make_random_test_test(10)
}
