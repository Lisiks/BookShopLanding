import aiofiles
import aiofiles.os
import os.path

from uuid import uuid4
from fastapi import UploadFile


class FileManager:
    __image_file_dir_path = "App/static/images/"
    __demo_file_dir_path = "App/static/demo/"

    __image_file_web_path = "static/images/"
    __demo_file_web_path = "static/demo/"


    @classmethod
    async def save_image_file(cls, file: UploadFile) -> str:
        file_extension = os.path.splitext(file.filename)[1]
        file_code = str(uuid4())

        save_file_name = f"{file_code}{file_extension}"
        save_file_path = f"{cls.__image_file_dir_path}{save_file_name}"

        async with aiofiles.open(save_file_path, "wb") as save_file:
            file_data = await file.read()
            await save_file.write(file_data)

        return f"{cls.__image_file_web_path}{save_file_name}"


    @classmethod
    async def save_demo_file(cls, file: UploadFile) -> str:
        file_extension = os.path.splitext(file.filename)[1]
        file_code = str(uuid4())

        save_file_name = f"{file_code}{file_extension}"
        save_file_path = f"{cls.__demo_file_dir_path}{save_file_name}"

        async with aiofiles.open(save_file_path, "wb") as save_file:
            file_data = await file.read()
            await save_file.write(file_data)

        return f"{cls.__demo_file_web_path}{save_file_name}"


    @classmethod
    async def delete_image_file(cls, web_path: str) -> None:
        file_name = os.path.basename(web_path)

        dir_path = f"{cls.__image_file_dir_path}{file_name}"
        await aiofiles.os.remove(dir_path)


    @classmethod
    async def delete_demo_file(cls, web_path: str) -> None:
        file_name = os.path.basename(web_path)

        dir_path = f"{cls.__demo_file_dir_path}{file_name}"
        await aiofiles.os.remove(dir_path)

