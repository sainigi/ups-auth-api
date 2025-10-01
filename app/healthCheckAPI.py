from fastapi import status,  APIRouter

router = APIRouter(
    tags=["HealthCheck"],
    responses={404: {"description": "Not found"}},
)

@router.get('/', status_code=status.HTTP_200_OK)
def heath_check():
    return {"status": "ok"}