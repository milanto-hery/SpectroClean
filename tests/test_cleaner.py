import numpy as np
from spectro_clean.cleaner import clean_spectrogram, image_to_spectrogram

def test_clean_shape_and_dtype():
    raw = np.random.rand(200,300)
    out = clean_spectrogram(raw, target_shape=(128,256))
    assert out.shape == (128,256)
    assert out.dtype == np.float32

def test_clean_from_dict_wrapper():
    raw = {'data': np.random.rand(100,100)}
    out = clean_spectrogram(raw, target_shape=(64,64))
    assert out.shape == (64,64)

def test_image_to_spec():
    img = np.random.randint(0,255,size=(50,100,3), dtype=np.uint8)
    spec = image_to_spectrogram(img)
    assert spec.ndim == 2
