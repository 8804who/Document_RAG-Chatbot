from fastapi import APIRouter, HTTPException
from ....core import auth
import logging

users_router = APIRouter()


@users_router.post("/login")
def login(username: str, password: str):
    auth.login()
    return True
