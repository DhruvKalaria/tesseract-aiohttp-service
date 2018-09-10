from .logging import logging_factory
from .validation import validation_factory

from aiohttp import web
from aiohttp.web_exceptions import HTTPUnprocessableEntity, HTTPRequestEntityTooLarge


def logging_middleware_factory(root_directory):
    logger = logging_factory(root_directory)

    async def logging_middleware_instance(app, handler):
        async def logging_handler(request):
            try:
                response = await handler(request)
                logger(request, response)
                return response
            except:
                raise

        return logging_handler

    return logging_middleware_instance


def validation_middleware_factory(root_directory):
    validator = validation_factory(root_directory)

    async def validation_middleware_instance(app, handler):
        async def validation_handler(request):
            try:
                validated_request = await validator(request)
                return await handler(validated_request)
            except HTTPRequestEntityTooLarge:
                return web.json_response(
                    {
                        "status": 413,
                        "message": "Maximum processable file size is 10 MB",
                    },
                    status=413,
                )
            except:
                return web.json_response(
                    {
                        "status": 422,
                        "message": "Unable to process request due to invalid document",
                    },
                    status=422,
                )

        return validation_handler

    return validation_middleware_instance
