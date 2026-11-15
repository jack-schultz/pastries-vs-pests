from app.window import Window


def run_tests() -> bool:
    """
    Runs the pytest file and returns True when every test passed
    :return: bool
    """
    import pytest
    return pytest.main() == 0


if run_tests():
    Window().run()
