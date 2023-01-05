from abc import ABC, abstractmethod
from typing import Union, Tuple, Optional
from numpy import ndarray, pi, cos, radians, sin, full_like

from .utils import create_2D_grid


class Elementary2DSolution(ABC):
    """
    All elementary solutions can be defined from this base class
    """

    TYPE = "elemental"

    def __init__(self, location: Tuple[Union[int, float], Union[int, float]], strength: Union[int, float]):
        """
        All elementary solutions are determined by its location and strength, hence, those parameters are required.

        Args:
            location: coordinates of the solution (X and Y).
            strength: strength of the solution.
        """
        self.x_orig, self.y_orig = location
        self.strength = strength

    @abstractmethod
    def compute_flow_field(self, grid: ndarray): ...


class SourceSink(Elementary2DSolution):
    def __init__(self):
        super().__init__()
        self.name = "source" if self.strength > 0 else "sink"

    def compute_flow_field(self, grid: Tuple[ndarray, ndarray]) -> Tuple[ndarray, ndarray]:
        """
        Computes the flow velocity in both directions (X and Y) on the points given by the grid argument. If the
        given strength was positive, the current instance will act as a source, while if it was negative will act as
        a sink.

        Args:
            grid: tuple containing two Numpy arrays indicating the X and Y coordinate of the grid nodes respectively.

        Returns:
            flow_velocity: Velocity in X and Y respectively for the current source/sink instance at the given grid
            nodes.
        """
        X, Y = grid
        u_flow = self.strength / (2 * pi) * (X - self.x_orig) / ((X - self.x_orig)**2 + (Y - self.y_orig)**2)
        v_flow = self.strength / (2 * pi) * (Y - self.y_orig) / ((X - self.x_orig)**2 + (Y - self.y_orig)**2)
        flow_velocity = [u_flow, v_flow]
        return flow_velocity


class Doublet2D(Elementary2DSolution):
    def __init__(self):
        super().__init__()
        self.name = "doublet"

    def compute_flow_field(self, grid: Tuple[ndarray, ndarray]) -> Tuple[ndarray, ndarray]:
        """
        Computes the flow velocity in both directions (X and Y) on the points given by the grid argument. If the
        given strength was positive, the current instance will act as a source, while if it was negative will act as
        a sink.

        Args:
            grid: tuple containing two Numpy arrays indicating the X and Y coordinate of the grid nodes respectively.

        Returns:
            flow_velocity: Velocity in X and Y respectively for the current doublet instance at the given grid
            nodes.
        """
        X, Y = grid
        u_flow = -self.strength / (2 * pi) * (
                (X - self.x_orig)**2 - (Y - self.y_orig)**2) / ((X - self.x_orig)**2 + (Y - self.y_orig)**2)**2
        v_flow = -self.strength / (2 * pi) * 2 * (
                X - self.x_orig) * (Y - self.y_orig) / ((X - self.x_orig)**2 + (Y - self.y_orig)**2)**2
        flow_velocity = [u_flow, v_flow]
        return flow_velocity


class Vortex2D(Elementary2DSolution):
    def __init__(self):
        super().__init__()
        self.name = "vortex"

    def compute_flow_field(self, grid: Tuple[ndarray, ndarray]) -> Tuple[ndarray, ndarray]:
        """
        Computes the flow velocity in both directions (X and Y) on the points given by the grid argument. If the
        given strength was positive, the current instance will act as a source, while if it was negative will act as
        a sink.

        Args:
            grid: tuple containing two Numpy arrays indicating the X and Y coordinate of the grid nodes respectively.

        Returns:
            flow_velocity: Velocity in X and Y respectively for the current vortex instance at the given grid
            nodes.
        """
        X, Y = grid
        u_flow = self.strength / (2 * pi) * (Y - self.y_orig) / ((X - self.x_orig)**2 + (Y - self.y_orig)**2)
        v_flow = -self.strength / (2 * pi) * (X - self.x_orig) / ((X - self.x_orig)**2 + (Y - self.y_orig)**2)
        flow_velocity = [u_flow, v_flow]
        return flow_velocity


class Freestream2D:
    """
    Freestream flow object
    """

    TYPE = "freestream"

    def __init__(self, flow_velocity: Union[float, int], angle_of_incidence: Optional[int] = 0):
        """
        Set up the main parameters of the freestream based on its intensity (velocity) and angle of incidence.

        Args:
            flow_velocity: Intensity of the flow.
            angle_of_incidence: Angle of the flow, in degrees.
        """
        self.name = self.TYPE
        self.flow_velocity = flow_velocity
        self.angle_of_incidence = angle_of_incidence
        self.x_velocity = self.flow_velocity * cos(radians(self.angle_of_incidence))
        self.y_velocity = self.flow_velocity * sin(radians(self.angle_of_incidence))

    def compute_flow_field(self, grid: Tuple[ndarray, ndarray]) -> Tuple[ndarray, ndarray]:
        """
        Computes the flow velocity of the freestream in both directions (X and Y) on the points given by the grid
        argument.

        Args:
            grid: tuple containing two Numpy arrays indicating the X and Y coordinate of the grid nodes respectively.

        Returns:
            flow_velocity: Velocity in X and Y respectively for the current freestream.
        """
        X, Y = grid
        u_flow = full_like(X, self.x_velocity)
        v_flow = full_like(Y, self.y_velocity)
        flow_velocity = [u_flow, v_flow]
        return flow_velocity
