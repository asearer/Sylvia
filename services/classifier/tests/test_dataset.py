# classifier/tests/test_dataset.py

from classifier.src.dataset import load_synthetic_dataset

def test_synthetic_dataset_shape():
    X, y = load_synthetic_dataset(n_samples=100)
    assert X.shape == (100, 10)
    assert y.shape == (100,)
