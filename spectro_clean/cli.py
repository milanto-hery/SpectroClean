"""Console entrypoint for SpectroClean."""
import argparse
import numpy as np
from .cleaner import clean_spectrogram, image_to_spectrogram
import os
from PIL import Image

def _load_image(path):
    im = Image.open(path).convert('RGB')
    return np.array(im)

def main():
    parser = argparse.ArgumentParser(prog="spectroclean")
    parser.add_argument("input", help="Input file (npy, png, jpg)")
    parser.add_argument("--out", help="Output .npy path", default=None)
    parser.add_argument("--height", type=int, default=128)
    parser.add_argument("--width", type=int, default=256)
    parser.add_argument("--norm", choices=["minmax","standard"], default="minmax")
    args = parser.parse_args()

    path = args.input
    if path.endswith('.npy'):
        arr = np.load(path)
    else:
        arr = _load_image(path)
        arr = image_to_spectrogram(arr)

    cleaned = clean_spectrogram(arr, target_shape=(args.height, args.width), normalization=args.norm)
    out = args.out or (os.path.splitext(path)[0] + "_clean.npy")
    np.save(out, cleaned)
    print(f"Saved cleaned spectrogram to: {out}")


if __name__ == '__main__':
    main()
