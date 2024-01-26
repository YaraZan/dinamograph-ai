from fastapi import APIRouter
from api.v1 import dnm, user, marker, auth

"""
    Router v1
"""
v1_router = APIRouter(prefix='/v1')
v1_router.include_router(dnm.router)
v1_router.include_router(user.router)
v1_router.include_router(marker.router)
v1_router.include_router(auth.router)
