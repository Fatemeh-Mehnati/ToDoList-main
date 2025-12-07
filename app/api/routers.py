# app/api/routers.py

from fastapi import APIRouter

from app.api.controllers import project_controller
# بعداً task_controller رو هم اینجا اضافه می‌کنیم

router = APIRouter()

router.include_router(project_controller.router)
