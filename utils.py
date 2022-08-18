from math import cos, sin


def mph_to_meters_per_second(n: float) -> float:
    return n * (1 / 60) * (1 / 60) * (1.60934 / 1) * (1000 / 1)


def meters_to_feet(n: float) -> float:
    return n * 3.284


def feet_to_meters(n: float) -> float:
    return n * 0.3048


class VelocityVector:
    v: float
    v_x: float
    v_y: float

    def __init__(self, v: float, launch_angle: float):
        self.v = v
        self.v_x = v * cos(launch_angle)
        self.v_y = v * sin(launch_angle)
