from fastapi import APIRouter


router = APIRouter(prefix="/api/statistics", tags=["统计分析"])


@router.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "statistics api is running"}
