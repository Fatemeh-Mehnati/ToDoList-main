# app/main.py

from fastapi import FastAPI

from app.api.routers import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="ToDoList API",
        version="0.1.0",
    )

    # ثبت تمام routerها
    app.include_router(api_router)

    @app.get("/", tags=["Health"])
    def health_check():
        return {"status": "ok"}

    return app


app = create_app()
