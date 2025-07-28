from fastapi import FastAPI
from routers import services, appointments

app = FastAPI()

app.include_router(services.router)
app.include_router(appointments.router)
