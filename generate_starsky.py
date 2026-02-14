#!/usr/bin/env python
"""
Generate "Stars in the Sky" visualization for CrystalSpace.

A striking dark-themed visualization of binary inorganic crystal chemical space
for public lectures and presentations.

Usage:
    python generate_starsky.py --png                    # Generate PNG only
    python generate_starsky.py --gif                    # Generate GIF only
    python generate_starsky.py --png --gif              # Generate both
    python generate_starsky.py --gif --frames 120       # More frames (smoother)
    python generate_starsky.py --preview                # Show interactive preview
    python generate_starsky.py --kubrick                # Kubrick 2001-style zoom (30s)
    python generate_starsky.py --kubrick --duration 10  # Shorter zoom
"""

from fire import Fire
from pathlib import Path

from visualize_app.starsky_visualization import (
    create_starsky_figure,
    export_png,
    export_gif,
    export_kubrick_zoom,
)


def main(
    reduction: str = "umap",
    embedding: str = "mat2vec",
    png: bool = False,
    gif: bool = False,
    preview: bool = False,
    kubrick: bool = False,
    width: int = 1920,
    height: int = 1080,
    frames: int = 60,
    duration: float = 4.0,
    fps: int = 15,
    scale: float = 2.0,
    output_dir: str = "outputs",
):
    """
    Generate stars-in-the-sky visualization.

    Args:
        reduction: Reduction method (umap, tsne, pca)
        embedding: Embedding method (mat2vec, magpie, megnet16, oliynyk, skipatom, random_200)
        png: Export as PNG
        gif: Export as animated GIF
        preview: Show interactive preview in browser
        kubrick: Generate Kubrick 2001-style cinematic zoom (MP4 + GIF)
        width: Output width in pixels
        height: Output height in pixels
        frames: Number of frames for GIF (drift/sway animation)
        duration: Duration in seconds (for GIF or Kubrick zoom)
        fps: Frames per second for Kubrick zoom (default 15)
        scale: PNG scale factor (2.0 = double resolution)
        output_dir: Output directory
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Generate figure
    print(f"Creating visualization ({reduction} + {embedding})...")
    fig = create_starsky_figure(
        reduction_method=reduction,
        embedding_method=embedding,
    )

    # Generate outputs
    base_name = f"crystal_space_{reduction}_{embedding}"

    if png:
        export_png(
            fig,
            output_path=str(output_path / f"{base_name}.png"),
            width=width,
            height=height,
            scale=scale,
        )

    if gif:
        export_gif(
            fig,
            output_path=str(output_path / f"{base_name}.gif"),
            width=width,
            height=height,
            num_frames=frames,
            duration_seconds=duration,
        )

    if kubrick:
        # Use t-SNE + mat2vec for Kubrick zoom (user's preferred)
        kubrick_reduction = "tsne"
        kubrick_embedding = "mat2vec"
        print(f"Creating Kubrick zoom visualization ({kubrick_reduction} + {kubrick_embedding})...")
        kubrick_fig = create_starsky_figure(
            reduction_method=kubrick_reduction,
            embedding_method=kubrick_embedding,
        )
        samples_dir = output_path / "samples"
        samples_dir.mkdir(exist_ok=True)
        export_kubrick_zoom(
            kubrick_fig,
            output_dir=str(samples_dir),
            base_name=f"kubrick_zoom_{kubrick_reduction}_{kubrick_embedding}",
            width=width,
            height=height,
            duration_seconds=duration if duration != 4.0 else 30.0,  # Default 30s for Kubrick
            fps=fps,
            export_mp4=True,
            export_gif=True,
        )

    if preview:
        print("Opening interactive preview in browser...")
        fig.show()

    if not (png or gif or preview or kubrick):
        print("No output specified. Use --png, --gif, --kubrick, or --preview")
        print("Run with --help for more options")


if __name__ == "__main__":
    Fire(main)
