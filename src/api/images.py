from fastapi import APIRouter, BackgroundTasks, UploadFile

from src.services.images import ImageService

router = APIRouter(prefix="/images", tags=["изображения отелей"])


@router.post(
    "", summary="Изображения отелей", description="Загрузка и форматирование изображений отелей"
)
def upload_images(file: UploadFile, background_tasks: BackgroundTasks):
    ImageService().upload_images(file, background_tasks)
