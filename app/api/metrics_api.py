from fastapi import APIRouter
from app.services.business.metrics_service import MetricsService

router = APIRouter()
metrics_service = MetricsService()


@router.get("")
def get_metrics():
    return metrics_service.get_metrics()