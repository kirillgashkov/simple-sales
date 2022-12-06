import typer

from simple_sales.api.__main__ import api

typer_app = typer.Typer()

# See https://github.com/tiangolo/typer/issues/119#issuecomment-657245317.
typer_app.command()(api)


# Empty callback is needed to prevent Typer from creating a CLI application with a
# single function as the main CLI application, not as a command/subcommand.
@typer_app.callback()
def simple_sales():
    pass


if __name__ == "__main__":
    typer_app()
