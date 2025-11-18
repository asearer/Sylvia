from design_generator import DesignGenerator

def test_generate_design():
    gen = DesignGenerator()
    design = gen.generate({"factors":1})
    assert "design" in design
