from fastapi import APIRouter
from testing.endpoints import abm, chaos, acm, settings, virtual_machine

router = APIRouter()
router.include_router(abm.router)
router.include_router(acm.router)
router.include_router(chaos.router)
router.include_router(settings.router)
router.include_router(virtual_machine.router)