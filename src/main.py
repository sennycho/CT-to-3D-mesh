import os
import numpy as np
from loader import load_nifti, normalize_ct
from preprocess import preprocess_mask
from visualize import show_slice, show_mesh
from mesh_gen import mask_to_mesh, smooth_mesh, decimate_mesh

def main():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data")
    print("Looking for files in:", os.path.abspath(data_path))

    files = os.listdir(data_path)
    print("List:", files)

    # 1. Load NIfTI files
    print("[1] Loading CT volume & mask...")

    volume = load_nifti(os.path.join(data_path, "IMG_0059.nii"))
    mask = load_nifti(os.path.join(data_path, "MASK_0059.nii"))

    volume = normalize_ct(volume)
    mask = (mask > 0).astype(np.uint8)

    # 2. Mask preprocessing
    print("[2] Preprocessing mask...")
    mask = preprocess_mask(mask)

    # 3. Middle slice preview
    print("[3] Showing middle slice preview...")
    show_slice(volume, mask)

    # 4. Generate Mesh from Mask
    mesh = mask_to_mesh(mask)

    # Save raw mesh
    output_path = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(output_path, exist_ok=True)

    raw_path = os.path.join(output_path, "mesh_raw.stl")
    mesh.export(raw_path)
    print(f"Raw mesh saved to: {raw_path}")

    # 5. Smooth Mesh
    mesh_smooth = smooth_mesh(mesh, iterations=20)
    smooth_path = os.path.join(output_path, "mesh_smooth.stl")
    mesh_smooth.export(smooth_path)
    print(f"Smoothed mesh saved to: {smooth_path}")

    # 6. Decimate Mesh
    mesh_decimated = decimate_mesh(mesh_smooth, reduction_ratio=0.3)
    dec_path = os.path.join(output_path, "mesh_decimated.stl")
    mesh_decimated.export(dec_path)
    print(f"Decimated mesh saved to: {dec_path}")

    # 7. 3D view
    show_mesh(mesh_decimated)

if __name__ == "__main__":
    main()
