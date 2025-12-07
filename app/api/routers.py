from fastapi import APIRouter

from app.api.controllers import project_controller, task_controller

router = APIRouter()

router.include_router(project_controller.router)
router.include_router(task_controller.router)
