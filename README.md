# SpectroClean

SpectroClean is a tiny, dependency-light Python library to **clean, standardize, and normalize spectrograms** for machine learning pipelines and audio research.

## Features
- Pad/crop spectrograms to a target shape (optionally keep aspect ratio)
- Normalize amplitude (min-max or z-score)
- Strip common metadata wrappers (e.g. {'data': ...})
- Convert image files saved as spectrograms back to numeric arrays
- Batch cleaning helper and simple CLI

## Installation

Option A: install from local checkout (development):
```bash
pip install -e .
```

Option B: install from GitHub (when published):
```bash
pip install git+https://github.com/yourusername/SpectroClean.git
```

## Quick usage
```python
from spectro_clean import clean_spectrogram
import numpy as np

raw = np.random.randn(200,300)
clean = clean_spectrogram(raw, target_shape=(128,256), normalization='minmax')
```

## CLI
After installation you can run:
```bash
spectroclean path/to/spec.png --height 128 --width 256 --norm minmax
```

## Development & Tests
```bash
pip install -r dev-requirements.txt
pytest -q
```

## Publishing
See PUBLISH.md for step-by-step instructions to publish to TestPyPI and PyPI.
