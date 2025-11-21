import numpy as np
from typing import Tuple, Iterable, Union
import warnings

ArrayLike = Union[np.ndarray, list, Tuple]

def pad_or_crop(spec: np.ndarray, target_shape: Tuple[int,int], keep_aspect: bool = False) -> np.ndarray:
    """Pad or crop spectrogram to the given (H, W).
    If keep_aspect=True, rescale preserving aspect ratio (simple nearest-neighbor)
    then pad/crop to target.
    """
    spec = np.array(spec)
    if spec.ndim != 2:
        # try to squeeze channels
        spec = np.squeeze(spec)
    H, W = target_shape
    h, w = spec.shape

    if keep_aspect and (h,w) != (H,W):
        # simple rescale using np.repeat/resize via nearest neighbor
        scale_h = H / h
        scale_w = W / w
        # choose uniform scaling to keep aspect
        scale = min(scale_h, scale_w)
        new_h = max(1, int(round(h * scale)))
        new_w = max(1, int(round(w * scale)))
        spec = np.array(spec)
        # Resize by simple repeat (fast, dependency free)
        spec = np.repeat(np.repeat(spec, int(np.ceil(new_h / h)), axis=0)[:new_h,:],
                         int(np.ceil(new_w / w)), axis=1)[:,:new_w]
        h, w = spec.shape

    # Crop
    spec = spec[:H, :W]

    # Pad
    pad_h = max(0, H - spec.shape[0])
    pad_w = max(0, W - spec.shape[1])

    if pad_h > 0 or pad_w > 0:
        spec = np.pad(spec, ((0, pad_h), (0, pad_w)), mode="constant", constant_values=0)
    return spec


def normalize(spec: np.ndarray, method: str = "minmax") -> np.ndarray:
    spec = spec.astype(np.float32)
    if method == "minmax":
        mn = np.min(spec)
        mx = np.max(spec)
        if mx - mn == 0:
            return np.zeros_like(spec)
        return (spec - mn) / (mx - mn)
    if method == "standard" or method == "zscore":
        m = np.mean(spec)
        s = np.std(spec)
        if s == 0:
            return np.zeros_like(spec)
        return (spec - m) / s
    raise ValueError(f"Unknown normalization method: {method}")


def _unwrap_possible_dict(spec):
    if isinstance(spec, dict):
        for k in ["data", "spectrogram", "spec", "S"]:
            if k in spec:
                return spec[k]
    return spec


def clean_spectrogram(
    spec: ArrayLike,
    target_shape: Tuple[int,int] = (128, 256),
    normalization: str = "minmax",
    force_float32: bool = True,
    keep_aspect: bool = False
) -> np.ndarray:
    """Clean, standardize, and normalize a raw spectrogram-like input.
    - accepts numpy arrays, lists, or simple dict wrappers (e.g. {'data': array})
    - pads or crops to `target_shape`
    - normalizes amplitude with `normalization` (minmax or standard)
    - forces dtype to float32
    """
    spec = _unwrap_possible_dict(spec)
    spec = np.array(spec)

    if spec.ndim > 2:
        spec = np.squeeze(spec)

    if spec.size == 0:
        warnings.warn("Empty spectrogram provided; returning zeros.")
        spec = np.zeros(target_shape, dtype=np.float32)

    spec = pad_or_crop(spec, target_shape, keep_aspect=keep_aspect)
    spec = normalize(spec, method=normalization)

    if force_float32:
        spec = spec.astype(np.float32)

    return spec


def clean_batch(specs: Iterable[ArrayLike], **kwargs):
    """Clean an iterable of spectrograms. Returns a numpy array (N,H,W)."""
    cleaned = [clean_spectrogram(s, **kwargs) for s in specs]
    return np.stack(cleaned, axis=0)


def image_to_spectrogram(image: ArrayLike, channel: str = "grayscale") -> np.ndarray:
    """Convert an image-like array to a spectrogram-like 2D array.
    This is a convenience helper for users that saved spectrograms as images.
    - channel: 'grayscale' or 'luminance' or 'avg' to collapse channels.
    """
    arr = np.array(image)
    if arr.ndim == 3:
        if channel in ("grayscale", "luminance", "avg"):
            # simple collapse: average channels
            spec = np.mean(arr, axis=2)
        else:
            # try given channel name as index
            try:
                idx = int(channel)
                spec = arr[..., idx]
            except Exception:
                raise ValueError("Unknown channel option for image_to_spectrogram.")
    elif arr.ndim == 2:
        spec = arr
    else:
        raise ValueError("Unsupported image shape for conversion.")
    return spec.astype(np.float32)
