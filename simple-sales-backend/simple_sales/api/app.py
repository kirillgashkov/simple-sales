from fastapi import FastAPI

from simple_sales.api.dependencies.db import db
from simple_sales.api.routers import cities, employees, sessions, users

app = FastAPI()

app.include_router(cities.router)
app.include_router(employees.router)
app.include_router(sessions.router)
app.include_router(users.router)


@app.on_event("startup")
async def on_startup():
    await db.start()


@app.on_event("shutdown")
async def on_shutdown():
    await db.stop()
