"""CLI entry point for cat-facts."""

import typer

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main() -> None:
    """A CLI tool that wraps the cat-facts API."""
    typer.echo("Hello from cat-facts-cli!")


if __name__ == "__main__":
    app()
