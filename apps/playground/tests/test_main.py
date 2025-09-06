from apps.playground.src.main import main

def test_main(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hello from Playground app!" in captured.out
