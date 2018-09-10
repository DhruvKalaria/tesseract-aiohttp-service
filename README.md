NEEDS UPDATE:
This service hosts tesseract over python aiohttp server. Internally uses pyOCR wrapper over tesseract.
Run: gunicorn server:app --bind :8000 --worker-class aiohttp.GunicornUVLoopWebWorker --log-level=DEBUG
