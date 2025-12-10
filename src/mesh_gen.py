import numpy as np
from skimage import measure
import trimesh
import pyvista as pv

# 1. Mask → Raw Mesh (Marching Cubes)
def mask_to_mesh(mask, spacing=(1, 1, 1)):
    print("[4] Generating 3D mesh from mask (marching cubes)...")

    verts, faces, normals, values = measure.marching_cubes(
        mask.astype(np.float32),
        level=0.5,
        spacing=spacing
    )

    mesh = trimesh.Trimesh(
        vertices=verts,
        faces=faces,
        vertex_normals=normals,
        process=False
    )

    return mesh

# 2. Smoothing (Laplacian)
def smooth_mesh(mesh, iterations=20):
    print("[5] Smoothing mesh...")

    smoothed = mesh.copy()
    trimesh.smoothing.filter_laplacian(smoothed, iterations=iterations)

    return smoothed

# 3. Decimation (Simplify)
def decimate_mesh(mesh, reduction_ratio=0.05):
    print("[6] Decimating mesh...")

    # 1) Convert to PyVista mesh
    faces = np.hstack([
        np.full((mesh.faces.shape[0], 1), 3),  # face size indicator
        mesh.faces
    ]).astype(np.int32)

    pv_mesh = pv.PolyData(mesh.vertices, faces)

    # 2) Decimate
    target = 1 - reduction_ratio  # keep ratio
    decimated = pv_mesh.decimate_pro(target)

    # 3) Convert back to trimesh
    new_faces = decimated.faces.reshape(-1, 4)[:, 1:4]  # skip leading '3'
    new_vertices = decimated.points

    out_mesh = trimesh.Trimesh(vertices=new_vertices, faces=new_faces)

    return out_mesh


