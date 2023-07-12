'''
based on pyeit/visual/plot.py file 
needs to be in the same folder as the latter
'''

import os
import numpy as np
import matplotlib.pyplot as plt
from pyeit.mesh.external import load_mesh, place_electrodes_equal_spacing
from pyeit.visual.plot import create_mesh_plot
from pyeit.visual.plot_live import create_live_plot  # modified function to update plot in real time
import pyeit.eit.protocol as protocol
from pyeit.eit.jac import JAC
from pyeit.eit.fem import EITForward

    
# The example file is oriented in the following manner:
#   Left towards the X axis
#   Anterior direction towards the Y axis
# This allows the 2D mesh to be displayed in the radiological view with no transformations
simulation_mesh_filename = (
    "example_data\mesha06_bumpychestslice_radiological_view_both_lungs_1_0-3.ply" # external ply file needed to generate plot
)
n_electrodes = 16

current_dir = os.path.dirname(os.path.abspath(__file__))
sim_mesh = load_mesh(os.path.join(current_dir, simulation_mesh_filename))
electrode_nodes = place_electrodes_equal_spacing(sim_mesh, n_electrodes=16)
sim_mesh.el_pos = np.array(electrode_nodes)

fig, ax = plt.subplots()
create_mesh_plot(
    ax, sim_mesh, electrodes=electrode_nodes, coordinate_labels="radiological"
)

protocol_obj = protocol.create(
    n_electrodes, dist_exc=int(n_electrodes / 2), step_meas=1, parser_meas="std"
)
fwd = EITForward(sim_mesh, protocol_obj)
vh = fwd.solve_eit(perm=1)
vi = fwd.solve_eit(perm=sim_mesh.perm)

# Recon
# Set up eit object
pyeit_obj = JAC(sim_mesh, protocol_obj)
pyeit_obj.setup(p=0.5, lamb=0.001, method="kotre", perm=1, jac_normalized=False)

# # Dynamic solve simulated data
ds_sim = pyeit_obj.solve(vi, vh, normalize=False)
#solution = np.real(ds_sim)
plot_image=fig=ax=bg=[]

while True:

    solution = (np.random.randint(100,size=5733))/100  # creates random array to update image
        
    plot_image, ax, fig, bg = create_live_plot(
        ax,
        solution,
        pyeit_obj.mesh,
        fig,
        bg,
        plot_image,
        electrodes=electrode_nodes,
        coordinate_labels="radiological",
    )
    
       




