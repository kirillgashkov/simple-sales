import typer
import uvicorn

from simple_sales.app import app

typer_app = typer.Typer()


@typer_app.command()
def simple_sales() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    typer_app()
