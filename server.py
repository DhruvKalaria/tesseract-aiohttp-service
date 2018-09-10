from aiohttp import web
from os.path import join, dirname, realpath
from service import create_app

"""
This is the entry point for the request. Basic server initialization code.
"""

root_dir = dirname(realpath(__file__))
app = create_app(root_dir)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8000)

