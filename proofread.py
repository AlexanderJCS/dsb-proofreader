"""
Main entry point for the DSB spine head center proofreading tool.
"""

from pathlib import Path

from gui import FileSelectionGUI
from visualizer import SpineProofreadVisualizer
import payload


def load_and_visualize(file_path):
    """
    Load a DSB file and start the proofreading visualization.

    :param file_path: Path to the .dsb file
    """
    pld = payload.pld_load(file_path)
    original_head_centers_scaled = pld.head_centers * 1e9  # Convert m -> nm

    # Try to load the latest saved state from the DSB file
    input_path = Path(file_path)
    base_filename = f"{input_path.stem}_proofread"
    latest_csv = payload.get_latest_csv_from_dsb(file_path, base_filename)

    # Prepare initial state
    if latest_csv is not None:
        # Load from saved state
        print(f"Loading previous proofreading session from DSB file...")
        head_centers_scaled = latest_csv[['PosX', 'PosY', 'PosZ']].values
        labels = latest_csv['status'].tolist()
        spine_names = latest_csv['Name'].tolist()
        # Load radii if available in CSV
        radii = latest_csv['Radius'].tolist() if 'Radius' in latest_csv.columns else None
    else:
        # Start fresh
        print(f"Starting new proofreading session...")
        head_centers_scaled = original_head_centers_scaled.copy()
        labels = None
        spine_names = None
        radii = None

    # Do not scale the annotations. They are already scaled.

    # Generate output path (not directly used, DSB saves internally now)
    output_path = input_path.parent / f"{input_path.stem}_proofread.csv"

    # Create and run visualizer
    visualizer = SpineProofreadVisualizer(
        pld.dendrite_mesh,
        head_centers_scaled,
        output_path,
        psds=pld.psds,
        annotation=pld.annotation,
        original_head_centers=original_head_centers_scaled,
        dsb_filepath=file_path,
        initial_labels=labels,
        initial_spine_names=spine_names,
        initial_radii=radii
    )
    visualizer.run()


def main():
    """Main entry point for the proofreading tool."""
    gui = FileSelectionGUI()
    gui.run(on_start_callback=load_and_visualize)


if __name__ == "__main__":
    main()

