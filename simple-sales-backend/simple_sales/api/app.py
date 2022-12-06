import fastapi

from simple_sales.api.routers import cities, employees, sessions, users

app = fastapi.FastAPI()

app.include_router(cities.router)
app.include_router(sessions.router)
app.include_router(users.router)
app.include_router(employees.router)
