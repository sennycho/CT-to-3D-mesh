import nibabel as nib
import numpy as np

def load_nifti(path):
    nii = nib.load(path)
    data = nii.get_fdata()
    return data

def normalize_ct(volume):
    # CT windowing (common practice)
    volume = np.clip(volume, -1000, 400)
    volume = (volume - volume.min()) / (volume.max() - volume.min())
    return volume
