# SpectroClean

SpectroClean is a tiny, dependency-light Python library to **clean, standardize, and normalize spectrograms** for machine learning pipelines and audio research.

## Features
- Pad/crop spectrograms to a target shape (optionally keep aspect ratio)
- Normalize amplitude (min-max or z-score)
- Strip common metadata wrappers (e.g. {'data': ...})
- Convert image files saved as spectrograms back to numeric arrays
- Batch cleaning helper and simple CLI

## Installation

Install from PyPI:

```bash
pip install spectroclean
```

Install from local checkout:

```bash
git clone https://github.com/milanto-hery/SpectroClean.git
cd SpectroClean
pip install -e .
```

## Quick usage
```python
from spectro_clean import clean_spectrogram
import numpy as np

raw = np.random.randn(200,300)
clean = clean_spectrogram(raw, target_shape=(128,256), normalization='minmax')
```

## CLI
After installation, you can run:
```bash
spectroclean path/to/spec.png --height 128 --width 256 --norm minmax
```

