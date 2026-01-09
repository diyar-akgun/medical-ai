"""
Quantitative MRI analysis for Ventricular-to-Brain Volume Ratio (VBR)
"""

import numpy as np

def compute_vbr(ventricular_volume, brain_volume):
    """
    Compute Ventricular-to-Brain Ratio (VBR) as percentage.
    """
    return (ventricular_volume / brain_volume) * 100


if __name__ == "__main__":
    # Example values (mean volumes)
    ventricular_volume = 183.3
    brain_volume = 1000.0

    vbr = compute_vbr(ventricular_volume, brain_volume)
    print(f"Computed VBR: {vbr:.2f}%")
