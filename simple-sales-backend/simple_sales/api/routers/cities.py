import fastapi

router = fastapi.APIRouter()


@router.get("/cities")
def get_cities() -> None:
    ...
