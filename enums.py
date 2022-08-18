from math import cos, pow, sin
from enum import Enum

from const import BASEBALL_MASS, CROSS_SECTIONAL_AREA, DRAG_COEFFICIENT
from utils import VelocityVector


class CelestialBody(Enum):
    # gravitational constant is relative to earth
    # https://galileo.phys.virginia.edu/classes/152.mf1i.spring02/GravityFactSheet.htm
    # air density is kg/m^3
    # http://btc.montana.edu/ceres/malcolm/cd/html/orbitsfacts.html
    mercury = {"g": 0.378, "air_density": 0.0002}
    venus = {"g": 0.894, "air_density": 65}
    earth = {"g": 1, "air_density": 1.23}
    mars = {"g": 0.379, "air_density": 0.020}
    jupiter = {"g": 2.54, "air_density": 0.16}
    saturn = {"g": 1.07, "air_density": 0.19}
    uranus = {"g": 0.8, "air_density": 0.42}
    neptune = {"g": 1.2, "air_density": 0.45}
    pluto = {"g": 0.059, "air_density": 0}
    # non-planets
    moon = {"g": 0.166, "air_density": 0}
    sun = {"g": 28, "air_density": 0}

    def get_name(self) -> str:
        overrides = {
            CelestialBody.moon: "the Moon",
            CelestialBody.sun: "the Sun",
        }

        return overrides.get(self, self.name.title())

    def gravitational_force(self) -> float:
        return 9.8 * self.value["g"]

    def air_density(self) -> float:
        return self.value["air_density"]
