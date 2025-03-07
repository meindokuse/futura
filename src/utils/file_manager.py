from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from contextlib import asynccontextmanager
from botocore.config import Config

from fastapi import HTTPException


class S3Client:
    def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()
        self.s3_config = Config(
            region_name="gis-1",
            s3={"addressing_style": "virtual"},  # Включение виртуального хостинга
        )

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config, config=self.s3_config) as client:
            yield client

    async def upload_file(
            self,
            file: bytes,
            file_id: int,
            category: str,
            expansion: str,
    ):
        """
        Загружает файл в S3 и возвращает ссылку на файл.
        """
        # Генерируем уникальное имя файла
        object_name = f"{category}_{file_id}.{expansion}"

        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file,

                )
                print(f"File {object_name} uploaded to {self.bucket_name}")
                return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_file(self, category: str, file_id: int, expansion: str):

        """
        Удаляет файл из S3.
        """
        object_name = f"{category}_{file_id}.{expansion}"
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # async def get_presigned_url(self, category: str, file_id: int):
    #     filename = f"{category}_{file_id}"
    #     async with self.get_client() as client:
    #         try:
    #             presigned_url = await client.generate_presigned_url(
    #                 "get_object",
    #                 Params={"Bucket": self.bucket_name, "Key": filename},
    #                 ExpiresIn=3600  # Срок действия ссылки в секундах
    #             )
    #             return {"url": presigned_url}
    #         except Exception as e:
    #             raise HTTPException(status_code=500, detail=str(e))

    async def get_presigned_url(self, category: str, file_id: int, expansion: str):
        object_name = f"{category}_{file_id}.{expansion}"
        async with self.get_client() as client:
            try:
                presigned_url = await client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self.bucket_name, "Key": object_name},
                    ExpiresIn=3600,  # Срок действия ссылки
                )
                return {"url": presigned_url}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    async def update_file(self,
                          file: bytes,
                          file_id: int,
                          category: str,
                          expansion: str,
                          ):
        try:
            await self.delete_file(category, file_id, expansion)
            await self.upload_file(file, file_id, category, expansion)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# from aiobotocore.session import get_session
# from botocore.config import Config
# from fastapi import HTTPException
#
# class S3ClientTest:
#     def __init__(self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str):
#         self.config = {
#             "aws_access_key_id": access_key,
#             "aws_secret_access_key": secret_key,
#             "endpoint_url": endpoint_url,
#         }
#         self.bucket_name = bucket_name
#         self.session = get_session()
#         self.s3_config = Config(
#             region_name="gis-1",
#             s3={"addressing_style": "virtual"},  # Включение виртуального хостинга
#         )
#
#     async def get_presigned_url(self, category: str, file_id: int):
#         filename = f"{category}_{file_id}"
#         async with self.session.create_client(
#             "s3",
#             **self.config,
#             config=self.s3_config,  # Добавляем конфигурацию клиента
#         ) as client:
#             try:
#                 presigned_url = await client.generate_presigned_url(
#                     "get_object",
#                     Params={"Bucket": self.bucket_name, "Key": filename},
#                     ExpiresIn=3600,  # Срок действия ссылки
#                 )
#                 return {"url": presigned_url}
#             except Exception as e:
#                 raise HTTPException(status_code=500, detail=str(e))
