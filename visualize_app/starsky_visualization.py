"""
Stars in the Sky - Chemical Space Visualization

A striking dark-themed visualization of binary inorganic crystal chemical space
where materials appear as glowing stars against a space-like background.
"""

import os
import tempfile
from pathlib import Path
from typing import List, Dict

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import imageio


# Luminous color scheme for dark background
STARSKY_COLORS = {
    "0": "#808080",  # Dim gray (Unlikely)
    "1": "#00FF41",  # Neon green (Interesting)
    "2": "#FF3366",  # Bright magenta (Missing)
    "3": "#00BFFF",  # Cyan blue (Standard)
}

GLOW_COLORS = {
    "0": "rgba(128, 128, 128, 0.15)",
    "1": "rgba(0, 255, 65, 0.2)",
    "2": "rgba(255, 51, 102, 0.2)",
    "3": "rgba(0, 191, 255, 0.2)",
}


def create_glow_traces(
    df: pd.DataFrame,
    label: str,
    core_color: str,
    glow_color: str,
) -> List[go.Scatter3d]:
    """
    Create layered traces for a glow effect.

    Uses 3 layers per category:
    - Outer halo: Large markers, very low opacity
    - Middle glow: Medium markers, low opacity
    - Core star: Small markers, full opacity
    """
    df_label = df[df["label"] == label]

    if len(df_label) == 0:
        return []

    traces = []

    # Outer glow (halo)
    traces.append(go.Scatter3d(
        x=df_label["x"],
        y=df_label["y"],
        z=df_label["z"],
        mode="markers",
        marker=dict(size=12, color=glow_color, opacity=0.1),
        hoverinfo="skip",
        showlegend=False,
    ))

    # Middle glow
    traces.append(go.Scatter3d(
        x=df_label["x"],
        y=df_label["y"],
        z=df_label["z"],
        mode="markers",
        marker=dict(size=7, color=glow_color, opacity=0.3),
        hoverinfo="skip",
        showlegend=False,
    ))

    # Core star (bright center)
    traces.append(go.Scatter3d(
        x=df_label["x"],
        y=df_label["y"],
        z=df_label["z"],
        mode="markers",
        marker=dict(size=3, color=core_color, opacity=0.9),
        hoverinfo="skip",
        showlegend=False,
    ))

    return traces


def create_dark_space_layout() -> dict:
    """Create a dark 'space' themed layout with hidden axes."""
    return dict(
        paper_bgcolor="black",
        plot_bgcolor="black",
        scene=dict(
            bgcolor="black",
            xaxis=dict(
                showticklabels=False,
                title="",
                showgrid=False,
                zeroline=False,
                showline=False,
                visible=False,
                showbackground=False,
            ),
            yaxis=dict(
                showticklabels=False,
                title="",
                showgrid=False,
                zeroline=False,
                showline=False,
                visible=False,
                showbackground=False,
            ),
            zaxis=dict(
                showticklabels=False,
                title="",
                showgrid=False,
                zeroline=False,
                showline=False,
                visible=False,
                showbackground=False,
            ),
        ),
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
    )


def set_camera_position(fig: go.Figure, angle_name: str = "default") -> go.Figure:
    """
    Set camera position for different viewing angles.

    Args:
        fig: Plotly figure
        angle_name: One of 'default', 'top', 'side', 'front', 'diagonal'
    """
    camera_positions = {
        "default": {"eye": {"x": 1.5, "y": 1.5, "z": 1.2}},
        "top": {"eye": {"x": 0, "y": 0, "z": 2.5}},
        "side": {"eye": {"x": 2.5, "y": 0, "z": 0.3}},
        "front": {"eye": {"x": 0, "y": 2.5, "z": 0.3}},
        "diagonal": {"eye": {"x": 1.8, "y": 1.8, "z": 0.5}},
        "low": {"eye": {"x": 1.5, "y": 1.5, "z": 0.2}},
    }

    camera = camera_positions.get(angle_name, camera_positions["default"])
    camera["center"] = {"x": 0, "y": 0, "z": 0}
    camera["up"] = {"x": 0, "y": 0, "z": 1}

    fig.update_layout(scene_camera=camera)
    return fig


def create_starsky_figure(
    reduction_method: str = "umap",
    embedding_method: str = "mat2vec",
    camera_angle: str = "default",
) -> go.Figure:
    """
    Create the stars-in-the-sky visualization.

    Args:
        reduction_method: Dimensionality reduction method (umap, tsne, pca)
        embedding_method: Embedding method (mat2vec, magpie, etc.)

    Returns:
        Plotly Figure object
    """
    # Load data
    base_path = Path(__file__).parent
    embedding_path = base_path / f"assets/reduced_embeddings_3d/{reduction_method}_{embedding_method}_mean.pkl"
    label_path = base_path / "assets/df_binary_label.pkl"

    df_embedding = pd.read_pickle(embedding_path)
    df_embedding.columns = ["x", "y", "z"]
    df_embedding["formula"] = df_embedding.index

    df_labels = pd.read_pickle(label_path)
    df_labels["label"] = df_labels["label"].astype(str)

    df = df_embedding.join(df_labels)

    # Create figure with all glow traces
    fig = go.Figure()

    # Add traces for each label category
    for label in ["0", "1", "2", "3"]:
        traces = create_glow_traces(
            df, label,
            STARSKY_COLORS[label],
            GLOW_COLORS[label]
        )
        for trace in traces:
            fig.add_trace(trace)

    # Apply dark theme
    fig.update_layout(**create_dark_space_layout())

    # Set camera angle
    set_camera_position(fig, camera_angle)

    return fig


def export_png(
    fig: go.Figure,
    output_path: str = "outputs/crystal_space_starsky.png",
    width: int = 1920,
    height: int = 1080,
    scale: float = 2.0,
) -> None:
    """
    Export the figure as a high-resolution PNG.

    Args:
        fig: Plotly figure
        output_path: Output file path
        width: Image width in pixels
        height: Image height in pixels
        scale: Scale factor for higher quality
    """
    fig.write_image(
        output_path,
        format="png",
        width=width,
        height=height,
        scale=scale,
        engine="kaleido",
    )
    print(f"PNG saved to: {output_path}")


def generate_sway_camera_positions(
    num_frames: int = 60,
    sway_amplitude: float = 15.0,
    vertical_bob: float = 5.0,
    distance: float = 2.5,
) -> List[Dict]:
    """
    Generate camera positions for a slow drift/sway animation.

    The camera moves in a gentle Lissajous-like pattern:
    - Horizontal sway: sin(t)
    - Vertical bob: sin(2t) with smaller amplitude
    """
    camera_positions = []

    for i in range(num_frames):
        t = (i / num_frames) * 2 * np.pi

        # Horizontal angle (azimuth) - primary sway motion
        azimuth = np.radians(sway_amplitude * np.sin(t))

        # Vertical angle (elevation) - secondary bob motion
        elevation = np.radians(20 + vertical_bob * np.sin(2 * t))

        # Convert spherical to Cartesian coordinates
        eye_x = distance * np.cos(elevation) * np.sin(azimuth)
        eye_y = distance * np.cos(elevation) * np.cos(azimuth)
        eye_z = distance * np.sin(elevation)

        camera_positions.append({
            "eye": {"x": eye_x, "y": eye_y, "z": eye_z},
            "center": {"x": 0, "y": 0, "z": 0},
            "up": {"x": 0, "y": 0, "z": 1},
        })

    return camera_positions


def export_gif(
    fig: go.Figure,
    output_path: str = "outputs/crystal_space_starsky.gif",
    width: int = 1920,
    height: int = 1080,
    num_frames: int = 60,
    duration_seconds: float = 4.0,
) -> None:
    """
    Export the figure as an animated GIF with slow drift/sway motion.

    Args:
        fig: Plotly figure
        output_path: Output GIF path
        width: Frame width in pixels
        height: Frame height in pixels
        num_frames: Number of frames in the animation
        duration_seconds: Total duration of one animation cycle
    """
    # Calculate fps from duration
    fps = num_frames / duration_seconds

    # Generate camera positions
    camera_positions = generate_sway_camera_positions(num_frames=num_frames)

    # Create temporary directory for frames
    with tempfile.TemporaryDirectory() as tmpdir:
        frame_paths = []

        for i, camera in enumerate(camera_positions):
            # Update camera position
            fig.update_layout(scene_camera=camera)

            # Save frame
            frame_path = os.path.join(tmpdir, f"frame_{i:04d}.png")
            fig.write_image(
                frame_path,
                format="png",
                width=width,
                height=height,
                engine="kaleido",
            )
            frame_paths.append(frame_path)

            # Progress indicator
            print(f"Rendering frame {i+1}/{num_frames}", end="\r")

        print(f"\nCombining {num_frames} frames into GIF...")

        # Read frames and create GIF
        frames = [imageio.imread(path) for path in frame_paths]

        # Save as GIF
        imageio.mimsave(
            output_path,
            frames,
            format="GIF",
            fps=fps,
            loop=0,
        )

    print(f"GIF saved to: {output_path}")


def generate_kubrick_zoom_positions(
    num_frames: int = 450,
    start_distance: float = 8.0,
    end_distance: float = 0.2,
    azimuth_deg: float = 45.0,
    elevation_deg: float = 25.0,
) -> List[Dict]:
    """
    Generate camera positions for Kubrick 2001-style cinematic zoom.

    The camera starts far from the materials galaxy and slowly zooms
    in and through it, with ease-in-out motion for cinematic feel.

    Args:
        num_frames: Total number of frames
        start_distance: Starting distance from center (far)
        end_distance: Ending distance from center (close/inside)
        azimuth_deg: Horizontal angle in degrees
        elevation_deg: Vertical angle in degrees
    """
    camera_positions = []

    azimuth = np.radians(azimuth_deg)
    elevation = np.radians(elevation_deg)

    for i in range(num_frames):
        # Normalized time [0, 1]
        t = i / (num_frames - 1)

        # Ease-in-out using smoothstep function for cinematic feel
        # Slow at start, faster in middle, slow at end
        t_eased = t * t * (3 - 2 * t)

        # Interpolate distance with easing
        distance = start_distance + (end_distance - start_distance) * t_eased

        # Convert spherical to Cartesian coordinates
        eye_x = distance * np.cos(elevation) * np.sin(azimuth)
        eye_y = distance * np.cos(elevation) * np.cos(azimuth)
        eye_z = distance * np.sin(elevation)

        camera_positions.append({
            "eye": {"x": eye_x, "y": eye_y, "z": eye_z},
            "center": {"x": 0, "y": 0, "z": 0},
            "up": {"x": 0, "y": 0, "z": 1},
        })

    return camera_positions


def export_kubrick_zoom(
    fig: go.Figure,
    output_dir: str = "outputs/samples",
    base_name: str = "kubrick_zoom_tsne_mat2vec",
    width: int = 1920,
    height: int = 1080,
    duration_seconds: float = 30.0,
    fps: int = 15,
    export_mp4: bool = True,
    export_gif: bool = True,
) -> None:
    """
    Export Kubrick 2001-style cinematic zoom as MP4 and/or GIF.

    Args:
        fig: Plotly figure
        output_dir: Output directory
        base_name: Base filename (without extension)
        width: Frame width in pixels
        height: Frame height in pixels
        duration_seconds: Total duration in seconds
        fps: Frames per second
        export_mp4: Whether to export MP4
        export_gif: Whether to export GIF
    """
    num_frames = int(duration_seconds * fps)

    print(f"Generating {num_frames} frames for {duration_seconds}s Kubrick zoom...")

    # Generate camera positions
    camera_positions = generate_kubrick_zoom_positions(num_frames=num_frames)

    # Create temporary directory for frames
    with tempfile.TemporaryDirectory() as tmpdir:
        frame_paths = []

        for i, camera in enumerate(camera_positions):
            # Update camera position
            fig.update_layout(scene_camera=camera)

            # Save frame
            frame_path = os.path.join(tmpdir, f"frame_{i:04d}.png")
            fig.write_image(
                frame_path,
                format="png",
                width=width,
                height=height,
                engine="kaleido",
            )
            frame_paths.append(frame_path)

            # Progress indicator
            pct = (i + 1) / num_frames * 100
            print(f"Rendering frame {i+1}/{num_frames} ({pct:.1f}%)", end="\r")

        print(f"\nRendering complete. Processing video...")

        # Read all frames
        frames = [imageio.imread(path) for path in frame_paths]

        # Export MP4
        if export_mp4:
            mp4_path = os.path.join(output_dir, f"{base_name}.mp4")
            print(f"Creating MP4: {mp4_path}")
            imageio.mimsave(
                mp4_path,
                frames,
                fps=fps,
                codec="libx264",
                quality=8,
            )
            print(f"MP4 saved to: {mp4_path}")

        # Export GIF (no loop)
        if export_gif:
            gif_path = os.path.join(output_dir, f"{base_name}.gif")
            print(f"Creating GIF: {gif_path}")
            imageio.mimsave(
                gif_path,
                frames,
                format="GIF",
                fps=fps,
                loop=1,  # Play once, don't loop
            )
            print(f"GIF saved to: {gif_path}")
