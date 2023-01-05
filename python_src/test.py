from plot.flowfield import plot_flowfield
from base.elementary import Freestream2D, SourceSink, Vortex2D, Doublet2D
from base.utils import create_2D_grid


grid = create_2D_grid(width=10, height=5, resolution=50)
freestream = Freestream2D(flow_velocity=1, angle_of_incidence=10)
freestream_velocity = freestream.compute_flow_field(grid)
source = SourceSink(location=[-1, 0], strength=2)
source_velocity = source.compute_flow_field(grid)
sink = SourceSink(location=[1, 0], strength=-3)
sink_velocity = source.compute_flow_field(grid)
flow_velocity = source_velocity + sink_velocity
plot_flowfield(grid, flow_velocity, geometry=([source.x_orig, source.y_orig], [sink.x_orig, sink.y_orig]))
