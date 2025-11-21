import numpy as np
from spectro_clean import clean_spectrogram

if __name__ == '__main__':
    raw = np.random.randn(220, 330)
    clean = clean_spectrogram(raw, target_shape=(128,256), normalization='minmax', keep_aspect=True)
    print('clean shape:', clean.shape)
