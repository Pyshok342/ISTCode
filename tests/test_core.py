from my_python_library import hello


def test_hello() -> None:
    assert hello("Alex") == "Hello, Alex!"
