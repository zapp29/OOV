"""Pytest module testing draw_table.py implementation."""
from src.oov.draw_table import build_table
from src.oov.oov import OOV


def test_draw_table(capsys):
    """Test if draw_table function returns a string or error."""
    res = OOV("typing").view_issubclass()
    try:
        build_table(res)
    except Exception:
        raise AssertionError()
    finally:
        pass
    captured = capsys.readouterr()
    assert isinstance(captured.out, str)
    assert len(captured.out) > 100
    assert len(captured.out.split("\n")) > 50
