from aiohttp import web
from aiohttp.web_exceptions import HTTPRequestEntityTooLarge

from ..common import convert_pdf_to_jpeg

from PIL import Image
import sys
import os
import pyocr
import pyocr.builders
import codecs


async def process_document(request):
    try:
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            sys.exit(1)
        tool = tools[0]
        name, extension = os.path.splitext(request["file_path"])
        if "pdf" in extension:
            images = convert_pdf_to_jpeg(request["file_path"])
            dict_pages = {}
            page_count = 0
            for image in images:
                txt = tool.image_to_string(
                    image, lang="eng", builder=pyocr.builders.TextBuilder()
                )
                dict_pages["page-" + str(page_count + 1)] = txt
                page_count += 1
            return web.json_response(dict_pages, status=200)
        else:
            txt = tool.image_to_string(
                Image.open(request["file_path"]),
                lang="eng",
                builder=pyocr.builders.TextBuilder(),
            )
        return web.json_response({"text": txt}, status=200)
    except SystemExit:
        return web.json_response(
            {"message": "Tesseract not installed or configured properly for OCR"},
            status=422,
        )
    except HTTPRequestEntityTooLarge:
        return web.json_response(
            {"message": "Maximum processable file size is 10 MB"}, status=413
        )
    except Exception as ex:
        raise ex
    finally:
        os.remove(request["file_path"])
