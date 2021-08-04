"""Command-line interface."""
import click

@click.command()
@click.argument("module", nargs=-1)
def main(module):
    click.echo(f"Hello {module}!")


if __name__ == "__main__":
    main()  # pragma: no cover
