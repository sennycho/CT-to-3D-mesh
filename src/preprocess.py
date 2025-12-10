import numpy as np
from scipy.ndimage import gaussian_filter, binary_closing, binary_opening

def preprocess_mask(mask):
    print("[2] Running mask preprocessing...")

    # 1. Smooth edges
    mask_smoothed = gaussian_filter(mask.astype(float), sigma=1)

    # 2. Threshold again to binary
    mask_binary = (mask_smoothed > 0.4).astype(np.uint8)

    # 3. Remove small holes
    mask_clean = binary_closing(mask_binary, iterations=2)

    # 4. Slight opening to smooth bump artifacts
    mask_clean = binary_opening(mask_clean, iterations=1)

    return mask_clean
