import uvicorn
from typer import Option, Typer

typer_app = Typer()


@typer_app.command()
def api(
    port: int = Option(8000, help="Port to run the server on."),
    reload: bool = Option(False, help="Reload the server when code changes."),
) -> None:
    # App is specified as a string to enable reloading.
    uvicorn.run("simple_sales.api.app:app", host="0.0.0.0", port=port, reload=reload)


if __name__ == "__main__":
    typer_app()
