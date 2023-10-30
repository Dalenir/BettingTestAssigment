from fastapi import APIRouter

first_router = APIRouter()


@first_router.get("/")
async def root():
    return {"message": "BetAPI is running"}
