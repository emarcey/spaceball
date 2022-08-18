from enums import CelestialBody
from space_ball_calculator import SpaceBallCalculator


def main() -> None:
    mph = 110
    deg = 35

    for b in CelestialBody:
        print(SpaceBallCalculator(mph, deg, b))


if __name__ == "__main__":
    main()
