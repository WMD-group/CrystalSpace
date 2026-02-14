#!/usr/bin/env python
"""
Generate sample stills and videos for the Stars in the Sky visualization.

Creates a folder of outputs including:
- PNG stills from different camera angles
- GIF animations with different styles
- Variations with different embedding methods
"""

from pathlib import Path
from visualize_app.starsky_visualization import (
    create_starsky_figure,
    export_png,
    export_gif,
    set_camera_position,
)


def main():
    output_dir = Path("outputs/samples")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Camera angles for stills
    angles = ["default", "top", "side", "front", "diagonal", "low"]

    # Embedding combinations to showcase
    embeddings = [
        ("umap", "mat2vec"),
        ("umap", "magpie"),
        ("tsne", "mat2vec"),
    ]

    print("=" * 60)
    print("Generating sample stills and videos")
    print("=" * 60)

    # 1. Generate stills from different angles (default embedding)
    print("\n[1/3] Generating PNG stills from different camera angles...")
    print("-" * 60)

    fig = create_starsky_figure(reduction_method="umap", embedding_method="mat2vec")

    for angle in angles:
        set_camera_position(fig, angle)
        output_path = output_dir / f"still_umap_mat2vec_{angle}.png"
        print(f"  Generating: {output_path.name}")
        export_png(fig, str(output_path), width=1920, height=1080, scale=2.0)

    # 2. Generate stills with different embeddings (default angle)
    print("\n[2/3] Generating PNG stills with different embeddings...")
    print("-" * 60)

    for reduction, embedding in embeddings:
        fig = create_starsky_figure(
            reduction_method=reduction,
            embedding_method=embedding,
            camera_angle="diagonal",
        )
        output_path = output_dir / f"still_{reduction}_{embedding}_diagonal.png"
        print(f"  Generating: {output_path.name}")
        export_png(fig, str(output_path), width=1920, height=1080, scale=2.0)

    # 3. Generate GIF animations
    print("\n[3/3] Generating GIF animations...")
    print("-" * 60)

    # Standard drift/sway GIF
    fig = create_starsky_figure(reduction_method="umap", embedding_method="mat2vec")
    output_path = output_dir / "animation_drift_60frames.gif"
    print(f"  Generating: {output_path.name} (this may take a few minutes)")
    export_gif(
        fig,
        str(output_path),
        width=1920,
        height=1080,
        num_frames=60,
        duration_seconds=4.0,
    )

    # Smaller/faster preview GIF
    output_path = output_dir / "animation_drift_preview.gif"
    print(f"  Generating: {output_path.name}")
    export_gif(
        fig,
        str(output_path),
        width=960,
        height=540,
        num_frames=30,
        duration_seconds=3.0,
    )

    print("\n" + "=" * 60)
    print("Done! All samples saved to: outputs/samples/")
    print("=" * 60)

    # List generated files
    print("\nGenerated files:")
    for f in sorted(output_dir.glob("*")):
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"  {f.name:<45} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
