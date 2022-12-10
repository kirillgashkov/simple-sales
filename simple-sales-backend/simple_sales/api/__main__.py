import uvicorn
from typer import Typer, Option

typer_app = Typer()


@typer_app.command()
def api(
    reload: bool = Option(False, help="Reload the server when code changes.")
) -> None:
    # App is specified as a string to enable reloading.
    uvicorn.run("simple_sales.api.app:app", host="0.0.0.0", port=8000, reload=reload)


if __name__ == "__main__":
    typer_app()
