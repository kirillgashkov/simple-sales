from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from simple_sales.api.dependencies.db import db
from simple_sales.api.routers import cities, employee_types, employees, sessions, users
from simple_sales.settings import API_CORS_ORIGINS

app = FastAPI()

app.include_router(cities.router)
app.include_router(employee_types.router)
app.include_router(employees.router)
app.include_router(sessions.router)
app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def remove_authenticate_basic_for_frontend(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    response = await call_next(request)

    is_request_from_frontend = (
        request.headers.get("X-Requested-With") == "XMLHttpRequest"
    )
    is_response_with_authenticate_basic = (
        response.headers.get("WWW-Authenticate") == "Basic"
    )

    if is_request_from_frontend and is_response_with_authenticate_basic:
        del response.headers["WWW-Authenticate"]

    return response


@app.on_event("startup")
async def on_startup() -> None:
    await db.start()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await db.stop()
