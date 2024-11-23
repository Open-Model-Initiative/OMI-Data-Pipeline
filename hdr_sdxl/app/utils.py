# SPDX-License-Identifier: Apache-2.0
import torch
import numpy as np


# Kurtosis
def calculate_kurtosis(tensor: torch.Tensor):
    mean = torch.mean(tensor)
    std = torch.std(tensor, unbiased=True)
    fourth_moment = torch.mean((tensor - mean) ** 4)
    kurtosis_val = fourth_moment / (std ** 4)
    return kurtosis_val - 3  # Subtract 3 for excess kurtosis (to make normal distribution kurtosis = 0)


# Mean Squared Deviation
def calculate_msd(tensor: torch.Tensor):
    mean = torch.mean(tensor)
    msd_value = torch.mean((tensor - mean) ** 2)
    return msd_value


# Dynamic Range
def calculate_dynamic_range(tensor: torch.Tensor, epsilon=1e-10):
    I_min = torch.min(tensor)
    I_max = torch.max(tensor)
    I_min = torch.clamp(I_min, min=epsilon)
    I_max = torch.clamp(I_max, min=epsilon)
    dynamic_range_db = 20 * torch.log10(I_max / I_min)
    return dynamic_range_db


# Entropy
def calculate_entropy(tensor: torch.Tensor):
    tensor = tensor.flatten()
    _unique_values, counts = torch.unique(tensor, return_counts=True)
    probabilities = counts.float() / counts.sum()
    entropy_value = -torch.sum(probabilities * torch.log2(probabilities))
    return entropy_value


def calculate_statistics(arr: np.ndarray):
    tensor = arr.astype(np.float32) / 65536.0
    tensor = torch.tensor(tensor, dtype=torch.float32).permute(2, 0, 1)
    kurtosis = calculate_kurtosis(tensor)
    msd = calculate_msd(tensor)
    dynamic_range = calculate_dynamic_range(tensor)
    entropy = calculate_entropy(tensor)
    dct = {
        "kurtosis": kurtosis.item(),
        "msd": msd.item(),
        "range": dynamic_range.item(),
        "entropy": entropy.item()
    }
    return dct
