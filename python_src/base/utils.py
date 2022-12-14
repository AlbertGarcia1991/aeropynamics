from numpy import linspace, meshgrid, ndarray, where, sqrt
from typing import Optional, Tuple


def create_2D_grid(
        width: int,
        height: int,
        x_orig: Optional[int] = None,
        y_orig: Optional[int] = None,
        resolution: Optional[int] = None
) -> ndarray:
    """
    Creates a bi-dimensional grid of the given width and height and with the given resolution, located on the given
    coordinates (left-bottom vertex of the rectangle). It is returned as a 2D Numpy array.

    Args:
        width: width of the grid as an integer value.
        height: height of the grid as an integer value.
        x_orig: location of the bottom edge of the grid. If not specified, the grid will be centered around 0 along the
            horizontal direction.
        y_orig: location of the left edge of the grid. If not specified, the grid will be centered around 0 along the
            vertical direction.
        resolution: Number of points along both directions. If not given, resolution will be equal to the maximum
            value between the given width and height.

    Returns:
        grid: Numpy array containing the 2D coordinates of the grid nodes. Can be unzipped as X, Y = create_2D_grid()
    """
    if x_orig is None:
        x_orig = -width / 2
    if y_orig is None:
        y_orig = -height / 2

    if not resolution:
        x = linspace(x_orig, x_orig + width, max(width, height))  # creates a 1D-array with the x-coordinates
        y = linspace(y_orig, y_orig + height, max(width, height))
    else:
        x = linspace(x_orig, x_orig + width, resolution)  # creates a 1D-array with the x-coordinates
        y = linspace(y_orig, y_orig + height, resolution)

    grid = meshgrid(x, y)

    return grid


def stagnation_points(flowfield: Tuple[ndarray, ndarray], tolerance: float = 1e-6) -> List[Tuple[ndarray, ndarray]]:
    """
    Search for stagnation points across the given flowfield defined as nodes where velocity modulues is below a
    certain threshold value.

    Args:
        flowfield: list containing the flow velocity in X and Y respectively as Numpy arrays.
        tolerance: max value of the velocity to be considered a stagnation point.

    Returns:
        stag_indices: list containing the X and Y indices, respectively, of every stagnation pont found.
    """
    mod_velocity = sqrt(flowfield[0]**2 + flowfield[1]**2)
    stag_indices = where(mod_velocity < tolerance)
    return stag_indices
