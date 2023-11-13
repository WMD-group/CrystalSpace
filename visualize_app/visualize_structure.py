import plotly.express as px
import plotly.graph_objects as go
from pymatgen.core import Structure
from pymatgen.core.periodic_table import Element
from visualize_app.assets.atom_colors import jmol_colors


def get_plotly_structure(structure: Structure = None) -> go.Figure:
    """
    Plot a pymatgen structure with its unit cell using plotly.
    Args:
        structure: pymatgen structure object.
        kwargs: additional keyword arguments.
    Returns:
        fig: plotly figure object.
    """
    if structure is None:
        return px.scatter_3d()

    # Getting atomic positions and species using list comprehension
    positions = [site.coords for site in structure]
    species = [str(site.specie) for site in structure]

    # Getting atomic colors
    atomic_colors = [jmol_colors[Element(specie).Z] for specie in species]

    # Getting atomic radii
    # atomic_radii = [float(Element(specie).atomic_radius) for specie in species]

    # Extracting x, y, and z coordinates
    x, y, z = zip(*positions)

    # Getting lattice vectors
    a, b, c = structure.lattice.matrix

    # Define lines for the unit cell
    lines = [
        [[0, 0, 0], a],
        [[0, 0, 0], b],
        [[0, 0, 0], c],
        [a, a + b],
        [a, a + c],
        [b, b + a],
        [b, b + c],
        [c, c + a],
        [c, c + b],
        [a + b, a + b + c],
        [a + c, a + c + b],
        [b + c, b + c + a],
    ]

    # scatter atoms
    trace_atoms = go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers",
        text=species,
        hoverinfo="text",
        marker=dict(
            symbol="circle",
            sizemode="diameter",
            color=atomic_colors,
            # size=[20 * r for r in atomic_radii],
            size=20,
            line=dict(color="black", width=5),
        ),
    )

    # draw unit cell
    trace_lines = []
    for line in lines:
        x_values, y_values, z_values = zip(*line)
        trace_lines.append(
            go.Scatter3d(
                x=x_values,
                y=y_values,
                z=z_values,
                mode="lines",
                line=dict(color="black"),
            )
        )

    # remove the background grid
    layout = go.Layout(
        scene=dict(
            xaxis=dict(
                showticklabels=False,
                title="",
                showgrid=False,
                zeroline=False,
                showline=False,
                visible=False,
            ),
            yaxis=dict(
                showticklabels=False,
                title="",
                showgrid=False,
                zeroline=False,
                showline=False,
                visible=False,
            ),
            zaxis=dict(
                showticklabels=False,
                title="",
                showgrid=False,
                zeroline=False,
                showline=False,
                visible=False,
            ),
        ),
        showlegend=False,
    )

    fig = go.Figure(data=[trace_atoms, *trace_lines], layout=layout)
    return fig
