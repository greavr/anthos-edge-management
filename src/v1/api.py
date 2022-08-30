from fastapi import APIRouter
from v1.endpoints import abm, chaos

router = APIRouter()
router.include_router(abm.router)
router.include_router(chaos.router)