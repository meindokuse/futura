from fastapi import APIRouter, HTTPException, UploadFile, File

from src.utils.file_manager import S3Client

router = APIRouter(
    tags=['files'],
    prefix='/files',
)


@router.post("/{category}/{file_id}/upload-photo")
async def upload_employer_photo(
        category: str,
        file_id: int,
        expansion: str,
        photo: UploadFile = File(...),
):
    try:
        file_manager = S3Client(
            access_key="4c1d4e098a6a4625a46af029860c5554",
            secret_key="c6e923640816445792206d378b9b7571",
            endpoint_url="https://s3.gis-1.storage.selcloud.ru",
            bucket_name="futura",
        )

        # Читаем файл
        file_content = await photo.read()

        # Загружаем файл в S3
        file_url = await file_manager.upload_file(file_content, file_id, category, expansion)

        return {
            'status': 'success',
            'file_url': file_url,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{category}/{file_id}/get-photo")
async def get_file_url(
        category: str,
        file_id: int,
        expansion: str,
):
    try:
        file_manager = S3Client(
            access_key="4c1d4e098a6a4625a46af029860c5554",
            secret_key="c6e923640816445792206d378b9b7571",
            endpoint_url="https://s3.gis-1.storage.selcloud.ru",
            bucket_name="futura",
        )
        # Загружаем файл в S3
        file_url = await file_manager.get_presigned_url(category, file_id, expansion)

        return {
            'status': 'success',
            'file_url': file_url,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{category}/{file_id}/delete-photo")
async def delete_file(category: str, file_id: int, expansion: str):
    try:
        file_manager = S3Client(
            access_key="4c1d4e098a6a4625a46af029860c5554",
            secret_key="c6e923640816445792206d378b9b7571",
            endpoint_url="https://s3.gis-1.storage.selcloud.ru",
            bucket_name="futura",
        )
        # Загружаем файл в S3
        await file_manager.delete_file(category, file_id, expansion)

        return {
            'status': 'success',
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
