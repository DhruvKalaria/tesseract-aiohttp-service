from aiohttp.web_exceptions import HTTPUnprocessableEntity, HTTPRequestEntityTooLarge
import json
import uuid
import os


def max_file_size():
    return 10000000


def validation_factory(root_directory):
    async def write_document(request):
        try:
            reader = await request.multipart()
            document = await reader.next()
            file_path = (
                root_directory + "/temp/" + uuid.uuid4().hex + "-" + document.filename
            )
            size = 0
            request["file_name"] = document.filename
            with open(file_path, "ab") as f:
                while True:
                    if size <= max_file_size():
                        data_chunk = await document.read_chunk()
                        if not data_chunk:
                            break
                        f.write(data_chunk)
                        size += len(data_chunk)
                    else:
                        os.remove(file_path)
                        raise HTTPRequestEntityTooLarge(
                            max_size=max_file_size(), actual_size=size
                        )
            request["root_directory"] = root_directory
            request["file_path"] = file_path
            return request
        except:
            raise

    async def validator(request):
        try:
            return await write_document(request)
        except:
            raise

    return validator
