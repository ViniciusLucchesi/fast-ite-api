from fastapi import FastAPI
from ite.routes import router as api_router


app = FastAPI(
    title="ITE Student FastAPI",
    version="0.1.0",
)


app.include_router(api_router)