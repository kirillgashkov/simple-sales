import typer
import uvicorn

typer_app = typer.Typer()


@typer_app.command()
def api(
    reload: bool = typer.Option(False, help="Reload the server when code changes.")
) -> None:
    # App is specified as a string to enable reloading.
    uvicorn.run("simple_sales.api.app:app", host="0.0.0.0", port=8000, reload=reload)


if __name__ == "__main__":
    typer_app()
