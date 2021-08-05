"""Command-line interface."""
import click


@click.command()
@click.argument(param_decls="module", nargs=-1)  # type: ignore
def main(module: str) -> None:
    """Main function."""
    click.echo(f"Hallo {module}!")


if __name__ == "__main__":
    main()  # pragma: no cover
