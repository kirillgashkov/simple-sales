import fastapi

from simple_sales.api.routers import users, sessions

app = fastapi.FastAPI()

app.include_router(users.router)
app.include_router(sessions.router)
