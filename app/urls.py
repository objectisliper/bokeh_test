from aiohttp import web

from app.views import MainView, JsForNone

url_list = [
        web.view("/", MainView),
        web.view("/plot.js", JsForNone),
    ]