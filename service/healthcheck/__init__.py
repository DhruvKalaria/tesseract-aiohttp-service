from aiohttp import web


async def status(request):
    return web.json_response({"host": request.host}, status=200)


def create_healthcheck_app(app_instance):
    app = app_instance(middlewares=[])
    app.router.add_get("/status", status)
    return app
