from fastapi import APIRouter
from .students import router as students_router


router = APIRouter()
router.include_router(students_router, prefix="/student", tags=["student"])