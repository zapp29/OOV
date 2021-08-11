"""Test cases for the __main__ module."""
import pytest
from click.testing import CliRunner

from oov.__main__ import main

# TODO: OOV can be used with: "python -m oov module1 module2"
# TODO: OOV can be used with: "oov module1 module2"


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(main, "dis")
    assert result.exit_code == 0


def test_console_entry(runner: CliRunner):
    """It exits with a status code of zero."""
    result = runner.invoke(main, "types")
    assert result.exit_code == 0
