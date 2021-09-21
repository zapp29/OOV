"""Command-line interface."""
import os
import sys
from typing import List

import click

from oov.draw_table import build_table
from oov.oov import OOV


@click.command()
@click.argument("modules", nargs=-1)  # type: ignore
def main(modules: List[str]):
    """Main function."""
    modules = list(modules)
    results = OOV(modules).view_issubclass()
    print("MODULES:", modules)
    build_table(results)


def console_entry() -> None:  # pragma: nocover
    """Console entry."""
    try:
        main()
        sys.stdout.flush()
        sys.stderr.flush()
    except BrokenPipeError:
        # Python flushes standard streams on exit; redirect remaining output
        # to devnull to avoid another BrokenPipeError at shutdown
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(2)


if __name__ == "__main__":
    console_entry()  # pragma: nocover
