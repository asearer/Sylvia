from bias_detector import BiasDetector

def test_bias_detector():
    bd = BiasDetector()
    result = bd.detect([1,2,3])
    assert "bias_detected" in result
