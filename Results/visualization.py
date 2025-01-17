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

# Plotting functions

def plot_orbit_plotly(motions, atmosphere_altitude=750, show_periandapo=False, atmoslayers=False):

    # Create a sphere for Earth
    earth_radius = 6371  # km
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x_earth = earth_radius * np.outer(np.cos(u), np.sin(v))
    y_earth = earth_radius * np.outer(np.sin(u), np.sin(v))
    z_earth = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))

    # Atmosphere radius
    atmosphere_radius = earth_radius + atmosphere_altitude

    # Calculate apo and periapsis NEEDS REVISION FOR DRAG ORBITS
    radii = np.sqrt(np.array(motions[:,0])**2 + np.array(motions[:,1])**2 + np.array(motions[:,2])**2)
    periapsis_idx = np.argmin(radii)
    apoapsis_idx = np.argmax(radii)
    periapsis_point = (motions[:,0][periapsis_idx], motions[:,1][periapsis_idx], motions[:,2][periapsis_idx])
    apoapsis_point = (motions[:,0][apoapsis_idx], motions[:,1][apoapsis_idx], motions[:,2][apoapsis_idx])

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

    if atmoslayers:
        # Add atmosphere layers with fading transparency
        num_layers = 20
        for i, alpha in enumerate(np.linspace(0.1, 0.01, num_layers)):
            layer_radius = earth_radius + (750 / num_layers) * i
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
    else:
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

    if show_periandapo:
        # Add apoapsis and periapsis points
        fig.add_trace(go.Scatter3d(
            x=[periapsis_point[0]], y=[periapsis_point[1]], z=[periapsis_point[2]],
            mode='markers',
            marker=dict(color='yellow', size=5),
            name="Periapsis"
        ))
        fig.add_trace(go.Scatter3d(
            x=[apoapsis_point[0]], y=[apoapsis_point[1]], z=[apoapsis_point[2]],
            mode='markers',
            marker=dict(color='orange', size=5),
            name="Apoapsis"
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


# Not fully functional
def plot_orbit_plotly_animated(motions, atmosphere_altitude=750):
    # Create Earth's surface
    earth_radius = 6371  # km
    u = np.linspace(0, 2 * np.pi, 50)  # Reduced resolution
    v = np.linspace(0, np.pi, 50)
    x_earth = earth_radius * np.outer(np.cos(u), np.sin(v))
    y_earth = earth_radius * np.outer(np.sin(u), np.sin(v))
    z_earth = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))

    # Atmosphere radius
    atmosphere_radius = earth_radius + atmosphere_altitude

    # Orbital path
    x_orbit = np.array(motions[:,0])[::10]  # Downsample data
    y_orbit = np.array(motions[:,1])[::10]
    z_orbit = np.array(motions[:,2])[::10]

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

    # Add a single atmosphere layer
    layer_radius = atmosphere_radius
    x_layer = layer_radius * np.outer(np.cos(u), np.sin(v))
    y_layer = layer_radius * np.outer(np.sin(u), np.sin(v))
    z_layer = layer_radius * np.outer(np.ones(np.size(u)), np.cos(v))
    fig.add_trace(go.Surface(
        x=x_layer,
        y=y_layer,
        z=z_layer,
        colorscale=[[0, 'blue'], [1, 'lightblue']],
        showscale=False,
        opacity=0.1,
    ))

    # Add static orbital path
    fig.add_trace(go.Scatter3d(
        x=x_orbit, y=y_orbit, z=z_orbit,
        mode='lines',
        line=dict(color='lightgreen', width=2),
        name="Orbit Path",
    ))

    # Add moving marker
    fig.add_trace(go.Scatter3d(
        x=[x_orbit[0]], y=[y_orbit[0]], z=[z_orbit[0]],
        mode='markers',
        marker=dict(color='red', size=3),
        name="Orbiting Object",
    ))

    # Create frames
    total_duration = 20000  # 20 seconds in milliseconds
    num_frames = len(x_orbit)
    frame_duration = total_duration // num_frames
    frames = [
        go.Frame(
            data=[
                go.Scatter3d(
                    x=[x_orbit[k]], y=[y_orbit[k]], z=[z_orbit[k]],
                    mode='markers',
                    marker=dict(color='red', size=3)
                )
            ]
        )
        for k in range(num_frames)
    ]

    fig.frames = frames

    # Add animation controls
    fig.update_layout(
        updatemenus=[{
            "type": "buttons",
            "buttons": [
                {"label": "Play", "method": "animate", "args": [None, {"frame": {"duration": frame_duration, "redraw": False}, "fromcurrent": True}]},
                {"label": "Pause", "method": "animate", "args": [[None], {"frame": {"duration": 0, "redraw": False}}]}
            ]
        }],
        scene=dict(
            xaxis=dict(
                title=dict(text='X (km)', font=dict(color='white')),
                tickfont=dict(color='white'),
                backgroundcolor='black',
                gridcolor='gray',
                zerolinecolor='gray'
            ),
            yaxis=dict(
                title=dict(text='Y (km)', font=dict(color='white')),
                tickfont=dict(color='white'),
                backgroundcolor='black',
                gridcolor='gray',
                zerolinecolor='gray'
            ),
            zaxis=dict(
                title=dict(text='Z (km)', font=dict(color='white')),
                tickfont=dict(color='white'),
                backgroundcolor='black',
                gridcolor='gray',
                zerolinecolor='gray'
            ),
            aspectmode='data',
            bgcolor='black'
        ),
        paper_bgcolor='black',
        font=dict(color='white'),
        margin=dict(l=0, r=0, b=0, t=0),
    )

    # Show plot
    fig.show()


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

