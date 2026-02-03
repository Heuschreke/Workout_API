from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from core.config import settings
from web import muscle_group, exercise, auth, user

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Настройка CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# app.include_router(user.router)
app.include_router(exercise.router)
app.include_router(muscle_group.router)
app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
def top():
    return {"message": "Welcome to Fitness Tracker API"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)