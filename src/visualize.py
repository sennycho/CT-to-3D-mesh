import matplotlib.pyplot as plt
import pyvista as pv

def show_slice(volume, mask=None, slice_idx=None):
    if volume.ndim != 3:
        raise ValueError("volume must be 3D")

    if slice_idx is None:
        slice_idx = volume.shape[2] // 2

    plt.imshow(volume[:, :, slice_idx], cmap="gray")
    if mask is not None:
        plt.imshow(mask[:, :, slice_idx], alpha=0.3, cmap="Reds")
    plt.title(f"Slice {slice_idx}")
    plt.show()

def show_mesh(mesh):
    print("[7] Opening 3D mesh viewer...")

    plotter = pv.Plotter()
    plotter.add_mesh(
        mesh,
        color="lightgray",
        opacity=1.0,
        smooth_shading=True
    )
    plotter.add_axes()
    plotter.show_grid()
    plotter.show()

