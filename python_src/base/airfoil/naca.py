from numpy import arctan, array, cos, linspace, ndarray, pi, power, sin, sqrt
from typing import Union


def naca4_gen(
        naca_series: Union[int, str],
        n: int,
        finite_te: bool = False,
        half_cos_space: bool = False
) -> ndarray:
    """
    Returns the coordinates of a NACA-4 series airfoil.

    Args:
        naca_series: unique number of the NACA airfoil. It must have a length of 4 digits or characters.
        n: number of points per side of the airfoil and without considering the leading edge. Hence,
            function will return 2*n+1 coordinate points as a list.
        finite_te: if False, it will generate a zero-thickness trailing edge (TE). Otherwise, will have a finite
            thickness.
        half_cos_space: if False, the space along x-axis (horizontal) between any two consecutive points on the same
            side will be the same value. Otherwise, the spice will follow an equispaced angle of the cosine function.

    Returns:
        coords: Numpy array containing the coordinates of the given NACA airfoil.

    References:
        https://github.com/dgorissen/naca/blob/master/naca.py
    """
    naca_series = str(naca_series) if isinstance(naca_series, int) else naca_series
    max_camber = float(naca_series[0]) / 100.
    dist_max_camber_to_le = float(naca_series[1]) / 10.
    max_thickness = float(naca_series[2:4]) / 100.

    if finite_te:
        a4 = -0.1015
    else:
        a4 = -0.1036

    # Compute the points along x-axis where we will return a coordinate point
    if half_cos_space:
        x_coords = [(0.5 * (1.0 - cos(xx))) for xx in linspace(0.0, pi, n + 1)]
    else:
        x_coords = linspace(0.0, 1.0, n + 1).tolist()

    # This list contains the thickness to cord from each x-axis coordinate point
    a0 = +0.2969
    a1 = -0.1260
    a2 = -0.3516
    a3 = +0.2843
    y_thickness = [
        5 * max_thickness * (
                a0 * sqrt(xx) + a1 * xx + a2 * power(xx, 2) + a3 * power(xx, 3) + a4 * power(xx, 4)) for xx in x_coords
    ]

    xc1 = [xx for xx in x_coords if xx <= dist_max_camber_to_le]
    xc2 = [xx for xx in x_coords if xx > dist_max_camber_to_le]

    if max_camber == 0:
        # Symmetric airfoil, so the thickness is the y-coordinate considering its sign
        yu = y_thickness
        yl = [-xx for xx in y_thickness]
        x_coords_final = x_coords[::-1] + x_coords[1:]
    else:
        yc1 = [max_camber / pow(dist_max_camber_to_le, 2) * xx * (2 * dist_max_camber_to_le - xx) for xx in xc1]
        yc2 = [
            max_camber / pow(
                1 - dist_max_camber_to_le, 2) * (1 - 2 * dist_max_camber_to_le + xx) * (1 - xx) for xx in xc2
        ]

        dyc1_dx = [max_camber / pow(dist_max_camber_to_le, 2) * (2 * dist_max_camber_to_le - 2 * xx) for xx in xc1]
        dyc2_dx = [max_camber / pow(1 - dist_max_camber_to_le, 2) * (2 * dist_max_camber_to_le - 2 * xx) for xx in xc2]
        theta = [arctan(xx) for xx in dyc1_dx + dyc2_dx]

        xu = [xx - yy * sin(zz) for xx, yy, zz in zip(x_coords, y_thickness, theta)]
        yu = [xx + yy * cos(zz) for xx, yy, zz in zip(yc1 + yc2, y_thickness, theta)]

        xl = [xx + yy * sin(zz) for xx, yy, zz in zip(x_coords, y_thickness, theta)]
        yl = [xx - yy * cos(zz) for xx, yy, zz in zip(yc1 + yc2, y_thickness, theta)]

        x_coords_final = xu[::-1] + xl[1:]

    y_coords_final = yu[::-1] + yl[1:]

    airfoil_coords = array([x_coords_final, y_coords_final])

    return airfoil_coords
