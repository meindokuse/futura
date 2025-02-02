
import uuid
from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from contextlib import asynccontextmanager

from fastapi import HTTPException


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
            self,
            file: bytes,
            file_name: str,
            category:str
    ):
        """
        Загружает файл в S3 и возвращает ссылку на файл.
        """
        # Генерируем уникальное имя файла
        object_name = f"{category}_{file_name}"

        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file,
                )
                print(f"File {object_name} uploaded to {self.bucket_name}")
                return True
        except ClientError as e:
            print(f"Error uploading file: {e}")
            raise

    async def delete_file(self, object_name: str):
        """
        Удаляет файл из S3.
        """
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                print(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            print(f"Error deleting file: {e}")
            raise

    async def get_presigned_url(self,filename: str):
        async with self.get_client() as client:
            try:
                presigned_url = await client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self.bucket_name, "Key": filename},
                    ExpiresIn=3600  # Срок действия ссылки в секундах
                )
                return {"url": presigned_url}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
