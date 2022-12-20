from fastapi import FastAPI
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


@app.on_event("startup")
async def on_startup() -> None:
    await db.start()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await db.stop()
