from asyncio import get_event_loop
from aiohttp import web, ClientSession

from .ocr import create_ocr_app
from .healthcheck import create_healthcheck_app
from .middleware import logging_middleware_factory, validation_middleware_factory

"""
This file registers different sub applications and injects them into main app.
"""


def service_application_factory():
    client_session = ClientSession(loop=get_event_loop())
    version = "1.0.0"

    def get_app_instance(middlewares=[]):
        app = web.Application(middlewares=middlewares)
        app["http_client"] = client_session
        app["app_version"] = version
        return app

    return get_app_instance


async def shutdown_http_client(app):
    await app["http_client"].close()


def create_app(root_directory):
    app_instance = service_application_factory()
    app = app_instance(middlewares=[logging_middleware_factory(root_directory)])
    app.on_cleanup.append(shutdown_http_client)

    app.add_subapp(
        "/ocr",
        create_ocr_app(root_directory, app_instance, validation_middleware_factory),
    )
    app.add_subapp("/healthcheck", create_healthcheck_app(app_instance))
    return app
