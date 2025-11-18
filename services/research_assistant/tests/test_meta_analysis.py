from meta_analysis import MetaAnalysis

def test_meta_analysis():
    ma = MetaAnalysis()
    result = ma.analyze([1,2,3])
    assert "meta_result" in result
