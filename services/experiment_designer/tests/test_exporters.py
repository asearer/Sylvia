from exporters import Exporter

def test_exporter():
    ex = Exporter()
    status = ex.export({"test": 123})
    assert status == "Export successful"
