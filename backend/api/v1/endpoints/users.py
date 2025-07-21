from fastapi import APIRouter, HTTPException
import logging

users_router = APIRouter()


@users_router.post("/")
def create_user():
    return "회원 가입"
