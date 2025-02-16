# Lucas Calderon
# This file contains functions to plot or visualize the results of the simulation.

import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import plotly.graph_objects as go

# ----------- ORBIT PLOTTING FUNCTIONS ------------

# Plot the orbit using Plotly
def plot_orbit_plotly(motions, res=0.5, atmosphere_altitude=750):

    """
    This function plots the orbit of the spacecraft using Plotly.
    The orbit is split into two segments: atmospheric and space.
    The atmospheric segment is colored red and the space segment is colored green.
    The Earth's surface is also plotted as a blue sphere.

    Parameters:
    - motions: a 3xN array containing the x, y, and z coordinates of the spacecraft at each time step.
    - res: the resolution of the plot. A value of 1 means that every point in the orbit is plotted.
    - atmosphere_altitude: the altitude of the atmosphere in km.

    Returns:
    - None
    """

    # Apply resolution
    step = int(1 / res)
    motions = motions[::step]

    # Create a sphere for Earth
    earth_radius = 6371 # km
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x_earth = earth_radius * np.outer(np.cos(u), np.sin(v))
    y_earth = earth_radius * np.outer(np.sin(u), np.sin(v))
    z_earth = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))

    # Atmosphere radius
    atmosphere_radius = earth_radius + atmosphere_altitude

    radii = np.sqrt(np.array(motions[:,0])**2 + np.array(motions[:,1])**2 + np.array(motions[:,2])**2)

    # Split orbit into atmosphere and space
    is_in_atmosphere = radii <= atmosphere_radius
    x_orbit, y_orbit, z_orbit = motions[:,0], motions[:,1], motions[:,2]

    def find_segments(mask):
        segments = []
        current_segment = []
        for i, in_mask in enumerate(mask):
            if in_mask:
                current_segment.append(i)
            elif current_segment:
                segments.append(current_segment)
                current_segment = []
        if current_segment:
            segments.append(current_segment)
        return segments
    
    atmosphere_segments = find_segments(is_in_atmosphere)
    space_segments = find_segments(~is_in_atmosphere)

    # Create figure
    fig = go.Figure()

    # Add Earth's surface
    fig.add_trace(go.Surface(
        x=x_earth,
        y=y_earth,
        z=z_earth,
        colorscale=[[0, 'blue'], [1, 'lightblue']],
        showscale=False,
        opacity=1.0,
    ))

    alpha = 0.1  # Transparency
    layer_radius = earth_radius + atmosphere_altitude
    x_layer = layer_radius * np.outer(np.cos(u), np.sin(v))
    y_layer = layer_radius * np.outer(np.sin(u), np.sin(v))
    z_layer = layer_radius * np.outer(np.ones(np.size(u)), np.cos(v))
    fig.add_trace(go.Surface(
        x=x_layer,
        y=y_layer,
        z=z_layer,
        colorscale=[[0, 'blue'], [1, 'lightblue']],
        showscale=False,
        opacity=alpha,
    ))

    # Add orbit segments - green for space, red for atmosphere
    for seg in space_segments:
        fig.add_trace(go.Scatter3d(
            x=x_orbit[seg],
            y=y_orbit[seg],
            z=z_orbit[seg],
            mode='lines',
            line=dict(color='lightgreen', width=2),
            name="Space Orbit",
            showlegend=False
        ))
    for seg in atmosphere_segments:
        fig.add_trace(go.Scatter3d(
            x=x_orbit[seg],
            y=y_orbit[seg],
            z=z_orbit[seg],
            mode='lines',
            line=dict(color='crimson', width=2),
            name="Atmospheric Orbit (h<750 km)",
            showlegend=False
        ))
    
    # Add custom legend entries for "Space Orbit" and "Atmospheric Orbit"
    fig.add_trace(go.Scatter3d(
        x=[None], y=[None], z=[None],
        mode='lines',
        line=dict(color='lightgreen', width=2),
        name="Space Orbit"
    ))
    fig.add_trace(go.Scatter3d(
        x=[None], y=[None], z=[None],
        mode='lines',
        line=dict(color='crimson', width=2),
        name="Atmospheric Orbit (h<750 km)"
    ))

    # Adjust layout
    fig.update_layout(
    scene=dict(
        xaxis=dict(
            title=dict(text='X (km)', font=dict(color='white')),  # Axis title font color
            tickfont=dict(color='white'),  # Axis tick font color
            backgroundcolor='rgba(0,0,0,0)'
        ),
        yaxis=dict(
            title=dict(text='Y (km)', font=dict(color='white')),
            tickfont=dict(color='white'),
            backgroundcolor='rgba(0,0,0,0)'
        ),
        zaxis=dict(
            title=dict(text='Z (km)', font=dict(color='white')),
            tickfont=dict(color='white'),
            backgroundcolor='rgba(0,0,0,0)'
        ),
        aspectmode='data',  # Ensures equal scaling
        bgcolor='black'  # Set the 3D scene background to black
    ),
    paper_bgcolor='black',  # Set outside area background to black
    font=dict(color='white'),  # General font color for the plot
    legend=dict(
        font=dict(color='white', size=12),  # Legend font color and size
        x=0.8,  # Adjust x position of the legend
        y=0.9   # Adjust y position of the legend
    ),
    margin=dict(l=0, r=0, b=0, t=0),  # Set margins
    )

    # Show plot
    fig.show()

# Plot the orbit using matplotlib
def plot_matplotlib(positions, t, state0, radial_event_states):
    # Plot results in a 3D plot
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Extract position components
    x, y, z = positions
    r = np.linalg.norm(positions, axis=0)

    # Extract positions of apoapsis and periapsis
    apoapsis_positions = [state[:3] for state in radial_event_states if np.linalg.norm(state[:3]) > np.linalg.norm(state0[:3])]
    periapsis_positions = [state[:3] for state in radial_event_states if np.linalg.norm(state[:3]) <= np.linalg.norm(state0[:3])]


    # Plot the trajectory
    ax.plot(x, y, z, label='Orbit trajectory')

    # Plot apoapsis and periapsis points
    for ap in apoapsis_positions:
        ax.scatter(*ap, color='red', s=100, label='Apoapsis')
    for pp in periapsis_positions:
        ax.scatter(*pp, color='green', s=100, label='Periapsis')

    # Plot Earth as a point at the origin
    ax.scatter(0, 0, 0, color='blue', s=200, label='Earth')

    # Add labels and legend
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Orbit Simulation')
    ax.legend()

    # Set aspect ratio
    ax.set_box_aspect([1, 1, 1])  # Equal scaling

    # Show the plot
    plt.show()

    # Plot altitude vs time
    plt.plot(t, r - 6371000)
    plt.show()

    print(len(t), 'time steps')


# ----------- COES PLOTTING FUNCTIONS ------------
def plot_coes(et:np.ndarray, coes:np.ndarray, save=False, relative=False, deg=False):

    """
    This function plots the classical orbital elements of the spacecraft over time.

    Inputs:
        et: The time of the simulation in seconds after J2000 as a 1xN element numpy array
        coes: The classical orbital elements of the spacecraft as a 11 element numpy array: 
            [peri, e, i, longitude_ascending_node, arg_periapsis, mean_anomaly_atepoch, epoch, mu, true_anomaly_atepoch, a, orbital_period] * N
        save: A boolean indicating whether to save the plot as a file

    Returns:
        None
    """

    # Normalize time to start at 0 and convert to hours
    et -= et[0]
    et = et / 3600  # Convert time to hours

    # Relative coes
    if relative:
        coes[:, 1] -= coes[0, 1]
        coes[:, 2] -= coes[0, 2]
        coes[:, 3] -= coes[0, 3]
        coes[:, 4] -= coes[0, 4]
        coes[:, 8] -= coes[0, 8]
        coes[:, 9] -= coes[0, 9]

    if deg:
        coes[:, 2] = np.degrees(coes[:, 2])
        coes[:, 3] = np.degrees(coes[:, 3])
        coes[:, 4] = np.degrees(coes[:, 4])
        coes[:, 8] = np.degrees(coes[:, 8])


    # Figure for the COEs
    fig,( ( ax0, ax1, ax2 ),( ax3, ax4, ax5 ) ) = plt.subplots( 2, 3, figsize = (12, 6) )
    if relative:
        fig.suptitle('Relative Classical Orbital Elements vs Time', fontsize = 20)

    else:
        fig.suptitle('Classical Orbital Elements vs Time', fontsize = 20)

    # True anomaly
    ax0.plot(et, coes[: , 8])
    ax0.set_xlabel('Time (hours)')
    if deg:
        ax0.set_ylabel('True Anomaly (deg)')
    else:
        ax0.set_ylabel('True Anomaly (rad)')
    ax0.grid( linestyle = 'dotted' )

    # Semi-major axis
    ax1.plot(et, coes[: , 9])
    ax1.set_xlabel('Time (hours)')
    ax1.set_ylabel('Semi-major Axis (km)')
    ax1.grid( linestyle = 'dotted' )

    # Eccentricity
    ax2.plot(et, coes[: , 1])
    ax2.set_xlabel('Time (hours)')
    ax2.set_ylabel('Eccentricity')
    ax2.grid( linestyle = 'dotted' )

    # Inclination
    ax3.plot(et, coes[: , 2])
    ax3.set_xlabel('Time (hours)')
    if deg:
        ax3.set_ylabel('Inclination (deg)')
    else:
        ax3.set_ylabel('Inclination (rad)')
    ax3.grid( linestyle = 'dotted' )

    # Right Ascension of the Ascending Node
    ax4.plot(et, coes[: , 3])
    ax4.set_xlabel('Time (hours)')
    if deg:
        ax4.set_ylabel('RAAN (deg)')
    else:
        ax4.set_ylabel('RAAN (rad)')
    ax4.grid( linestyle = 'dotted' )

    # Argument of Periapsis
    ax5.plot(et, coes[: , 4])
    ax5.set_xlabel('Time (hours)')
    if deg:
        ax5.set_ylabel('Argument of Periapsis (deg)')
    else:
        ax5.set_ylabel('Argument of Periapsis (rad)')
    ax5.grid( linestyle = 'dotted' )

    # Adjust the plots
    plt.subplots_adjust( hspace = 0.5, wspace = 0.3)

    # Save or show the plot
    if save:
        plt.savefig('coes_plot.png')

    plt.show()


# ----------- AIR COMPOSITION PLOTTING FUNCTIONS ------------

# Plot collected air composition
def plot_atmos_data(flows_hist, savepath=None):
    # Extract data
    labels = [key for key in flows_hist if key not in ('air_mass', 'name')]
    data = [sum(flows_hist[key]) for key in flows_hist if key not in ('air_mass', 'name')]

    # Dynamically generate colors based on the number of data points
    cmap = cm.get_cmap('tab10')  # Use 'tab10' for distinct colors, or try 'viridis', 'plasma', etc.
    colors = [cmap(i / len(labels)) for i in range(len(labels))]

    # Create the pie chart without labels
    wedges, texts, autotexts = plt.pie(
        data, autopct='%1.1f%%', startangle=140, colors=colors
    )
    plt.axis('equal')  # Ensures the pie chart is a circle

    # Add a legend to the right
    plt.legend(wedges, labels, title="Components", loc="center left", bbox_to_anchor=(1, 0.5))

    # Add a title
    plt.title('Captured Air Composition')

    # Adjust layout to accommodate legend
    plt.tight_layout()

    # Save or show the chart
    if savepath:
        plt.savefig(savepath)
    else:
        plt.show()








