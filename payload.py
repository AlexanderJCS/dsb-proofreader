import pickle
from dataclasses import dataclass
from datetime import datetime

import zipfile
import io

import numpy as np
import pandas as pd
import trimesh



@dataclass(frozen=True)
class Payload:
    dendrite_mesh: trimesh.Trimesh
    head_centers: np.ndarray
    annotation: list[tuple[np.ndarray, str]] | None
    psds: trimesh.Trimesh | None


def pld_save(pld: Payload, filepath: str) -> None:
    """
    Save the payload to a file.
    :param pld: The payload to save
    :param filepath: The path to save the payload to
    """

    stl_bytes = pld.dendrite_mesh.export(file_type="stl")
    head_centers_bytes = pickle.dumps(pld.head_centers)
    annotation_bytes = pickle.dumps(pld.annotation)
    psds_stl_bytes = pld.psds.export(file_type="stl") if pld.psds is not None else b""

    with zipfile.ZipFile(filepath, "w") as zf:
        zf.writestr("mesh.stl", stl_bytes)
        zf.writestr("head_centers.pickle", head_centers_bytes)
        zf.writestr("annotation.pickle", annotation_bytes)
        zf.writestr("psds.stl", psds_stl_bytes)


def pld_load(filepath: str) -> Payload:
    """
    Load the payload from a file.
    :param filepath: The path to load the payload from
    :return: The loaded payload
    """
    print(f"[PAYLOAD] Opening DSB file: {filepath}")
    with zipfile.ZipFile(filepath, "r") as zf:
        print(f"[PAYLOAD] Reading mesh.stl...")
        mesh_bytes = zf.read("mesh.stl")
        print(f"[PAYLOAD] Reading annotation.pickle...")
        annotation_bytes = zf.read("annotation.pickle")
        print(f"[PAYLOAD] Reading head_centers.pickle...")
        head_centers_bytes = zf.read("head_centers.pickle")
        print(f"[PAYLOAD] Reading psds.stl...")
        psds_bytes = zf.read("psds.stl")

    print(f"[PAYLOAD] Unpickling head_centers...")
    head_centers = pickle.loads(head_centers_bytes)
    print(f"[PAYLOAD] Loading dendrite mesh from STL...")
    dendrite_mesh = trimesh.load(io.BytesIO(mesh_bytes), force="mesh", file_type="stl")
    print(f"[PAYLOAD] Unpickling annotation...")
    annotation = pickle.loads(annotation_bytes)
    print(f"[PAYLOAD] Loading PSDs mesh...")
    psds = trimesh.load(io.BytesIO(psds_bytes), force="mesh", file_type="stl") if psds_bytes else None
    print(f"[PAYLOAD] All data loaded successfully")

    return Payload(
        dendrite_mesh=dendrite_mesh,
        annotation=annotation,
        psds=psds,
        head_centers=head_centers
    )


def save_csv_to_dsb(dsb_filepath: str, csv_data: pd.DataFrame, base_filename: str) -> str:
    """
    Save a CSV file to the DSB file with a timestamp.

    :param dsb_filepath: Path to the .dsb file
    :param csv_data: DataFrame containing the CSV data
    :param base_filename: Base name for the CSV file (without extension)
    :return: The filename used in the DSB
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"{base_filename}_{timestamp}.csv"

    # Convert DataFrame to CSV bytes
    csv_bytes = csv_data.to_csv(index=False).encode('utf-8')

    # Append to existing DSB file
    with zipfile.ZipFile(dsb_filepath, "a") as zf:
        zf.writestr(csv_filename, csv_bytes)

    return csv_filename


def get_latest_csv_from_dsb(dsb_filepath: str, base_filename: str) -> pd.DataFrame | None:
    """
    Get the latest CSV file from the DSB file based on timestamp.

    :param dsb_filepath: Path to the .dsb file
    :param base_filename: Base name for the CSV file (without timestamp)
    :return: DataFrame with the latest CSV data, or None if no CSV found
    """
    print(f"[PAYLOAD] Searching for CSV files with base: {base_filename}")
    with zipfile.ZipFile(dsb_filepath, "r") as zf:
        # Find all CSV files matching the base filename pattern
        csv_files = [name for name in zf.namelist()
                     if name.startswith(base_filename) and name.endswith('.csv')]

        if not csv_files:
            print(f"[PAYLOAD] No previous CSV files found")
            return None

        # Sort by timestamp (embedded in filename) to get the latest
        csv_files.sort(reverse=True)
        latest_csv = csv_files[0]
        print(f"[PAYLOAD] Found {len(csv_files)} CSV file(s), loading latest: {latest_csv}")

        # Read the CSV
        csv_bytes = zf.read(latest_csv)
        csv_data = pd.read_csv(io.BytesIO(csv_bytes))
        print(f"[PAYLOAD] CSV loaded with {len(csv_data)} rows")

        return csv_data
