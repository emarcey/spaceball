from math import cos, atan2, pow, radians, sin, sqrt

from const import CROSS_SECTIONAL_AREA, DRAG_COEFFICIENT, BASEBALL_MASS
from enums import CelestialBody
from utils import feet_to_meters, meters_to_feet, mph_to_meters_per_second, VelocityVector


class SpaceBallCalculator:
    initial_velocity: float
    initial_velocity_meters_per_second: float
    initial_velocity_vector: VelocityVector
    initial_height: float
    launch_angle: float
    planet: CelestialBody

    def __init__(self, initial_velocity: float, launch_angle: float, planet: CelestialBody, initial_height: float = 3):
        self.initial_velocity = initial_velocity
        self.initial_velocity_meters_per_second = mph_to_meters_per_second(self.initial_velocity)
        self.launch_angle = launch_angle
        self.launch_angle_radians = radians(launch_angle)
        self.initial_velocity_vector = VelocityVector(
            self.initial_velocity_meters_per_second, self.launch_angle_radians
        )
        self.initial_height = initial_height
        self.initial_height_meters = feet_to_meters(self.initial_height)

        self.planet = planet

    def drag(self, v: float, launch_angle: float) -> float:
        F = 0.5 * self.planet.air_density() * v * v * CROSS_SECTIONAL_AREA * DRAG_COEFFICIENT
        return (F * cos(launch_angle), F * sin(launch_angle))

    def distance_traveled_without_drag(self) -> float:
        flight_time = (
            self.initial_velocity_vector.v * sin(self.launch_angle_radians)
            + sqrt(
                pow(self.initial_velocity_vector.v * sin(self.launch_angle_radians), 2)
                + 2 * self.planet.gravitational_force() * self.initial_height_meters
            )
        ) / self.planet.gravitational_force()
        return self.initial_velocity_vector.v_x * flight_time

    def distance_traveled_with_drag(self) -> float:
        # https://physics.stackexchange.com/a/336696
        x = 0
        y = self.initial_height_meters
        v = self.initial_velocity_vector.v
        vx = self.initial_velocity_vector.v_x
        vy = self.initial_velocity_vector.v_y
        launch_angle = self.launch_angle_radians
        t = 0
        dt = 0.01
        X = [0]
        Y = [y]
        while (y > 0) | (vy > 0):
            # instantaneous force:
            Fx, Fy = self.drag(v, launch_angle)
            # acceleration:
            ax = -Fx / BASEBALL_MASS
            ay = -Fy / BASEBALL_MASS - self.planet.gravitational_force()
            # position update:
            x = x + vx * dt + 0.5 * ax * dt * dt
            y = y + vy * dt + 0.5 * ay * dt * dt
            # update velocity components:
            vx = vx + ax * dt
            vy = vy + ay * dt
            # new angle and velocity:
            v = sqrt(vx * vx + vy * vy)
            launch_angle = atan2(vy, vx)
            # store result for plotting:
            X.append(x)
            Y.append(y)
            t = t + dt

        ft = Y[-2] / (Y[-2] - Y[-1])

        return X[-2] + (X[-1] - X[-2]) * ft

    def distance_traveled(self) -> float:
        if self.planet.air_density() == 0:
            return self.distance_traveled_without_drag()
        return self.distance_traveled_with_drag()

    def __str__(self) -> str:
        dist = meters_to_feet(self.distance_traveled())
        dist_str = f"{round(dist, 2):,}"
        if dist < 1e-2:
            dist_str = f"{dist:.2e}"

        return f"A ball on {self.planet.get_name()}, hit at {round(self.initial_velocity,2)} MPH, and an angle of {self.launch_angle}°, would travel {dist_str} feet."
