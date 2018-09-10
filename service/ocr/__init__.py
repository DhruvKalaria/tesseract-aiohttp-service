from .document import process_document


def create_ocr_app(root_directory, app_instance, middleware_factory):
    app = app_instance(middlewares=[middleware_factory(root_directory)])
    app.router.add_post("/document", process_document)
    return app
