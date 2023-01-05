import matplotlib.pyplot as plt
from typing import Tuple, Optional, List, Union, Set
from numpy import ndarray, sqrt

from .format import greyscale_colours
from ..base.elementary import Elementary2DSolution
from ..base.airfoil.airfoil_base import Airfoil


def plot_flowfield(
        grid: Tuple[ndarray, ndarray],
        velocity: Optional[Tuple[ndarray, ndarray]] = None,
        geometry: Optional[Union[Union[Elementary2DSolution], List[Union[Elementary2DSolution]]]] = None,
        countour_level: Optional[Union[float, int]] = None,
        streamlines: bool = True,
        v_map: bool = False,
        cp_map: Optional[Union[float, int]] = None,  # If not None, this must indicate the freestream velocity
        title: Optional[str] = None
):
    plt.plot(figsize=(20, 10))
    if title:
        plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.xlim(grid[0].min(), grid[0].max())
    plt.ylim(grid[1].min(), grid[1].max())
    if velocity:
        if streamlines:
            plt.streamplot(
                grid[0], grid[1], velocity[0], velocity[1], density=2, linewidth=0.5, arrowsize=1, arrowstyle="->")
        if countour is not None:
            pyplot.contour(
                grid[0], grid[1], velocity, levels=[countour_level], colors='#CD2305', linewidths=2, linestyles='solid')
        if v_map:
            v_mod = sqrt(velocity[0]**2 + velocity[1]**2)
            v_map_plot = plt.contourf(
                grid[0], grid[1], v_mod, levels=numpy.linspace(min(v_mod), max(v_mod), 100), extend='both')
            v_map_bar = plt.colorbar(v_map_plot)
            v_map_bar.set_label('$V$', fontsize=16)
        if cp_map is not None:
            cp = 1. - (velocity[0]**2 + velocity[1]**2) / cp_map
            cp_map_plot = plt.contourf(
                grid[0], grid[1], cp, levels=numpy.linspace(min(cp), max(cp), 100), extend='both')
            cp_map_bar = plt.colorbar(cp_map_plot)
            cp_map_bar.set_label('$C_p$', fontsize=16)
    if geometry:
        if isinstance(geometry, list):
            for idx, g in enumerate(geometry):
                # TODO: Handle in a better way the sequential colours; they have to be different, idx might be
                #  greater than number of colours, and ideally can be indicated on legend
                match geometry.TYPE:
                    case "elemental":
                        plt.scatter(g.x_orig, g.y_orig, color=greyscale_colours[idx], marker="o", s=10)
                    case "freestream":
                        # TODO: Draw on bottom-left corner the velocity triangle of the freestream flow
                        pass
                    case "airfoil":
                        # TODO: Draw the airfoil body with lines
                        pass
                    case _:
                        raise NotImplementedError(f"Geometry fo type {geometry.TYPE} has not been implemented yet")
        else:
            match geometry.TYPE:
                case "elemental":
                    plt.scatter(geometry.x_orig, geometry.y_orig, color="black", marker="o", s=10)
                case "freestream":
                    # TODO: Draw on bottom-left corner the velocity triangle of the freestream flow
                    pass
                case "airfoil":
                    # TODO: Draw the airfoil body with lines
                    pass
                case _:
                    raise NotImplementedError(f"Geometry fo type {geometry.TYPE} has not been implemented yet")
    plt.show()
