from apps.classifier.src.main import main

def test_main(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hello from Classifier app!" in captured.out
