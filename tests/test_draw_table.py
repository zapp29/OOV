"""Pytest module testing draw_table.py implementation."""
import pytest
from src.oov.draw_table import build_table
from src.oov.oov import OOV


@pytest.fixture
def load_objects():
    """Fixture to initialize test scenarios."""
    return [
        OOV("itertools"),
        OOV("types"),
        OOV("dis"),
        OOV("typing", "types"),
        OOV("typing", "itertools"),
    ]


def test_draw_table():
    """Test draw_table function."""
    res = OOV("types").view_issubclass()
    build_table(res)
