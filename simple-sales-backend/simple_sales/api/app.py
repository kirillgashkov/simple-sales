from fastapi import FastAPI

from simple_sales.api.dependencies.db import db
from simple_sales.api.routers import cities, employee_types, employees, sessions, users

app = FastAPI()

app.include_router(cities.router)
app.include_router(employee_types.router)
app.include_router(employees.router)
app.include_router(sessions.router)
app.include_router(users.router)


@app.on_event("startup")
async def on_startup() -> None:
    await db.start()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await db.stop()
