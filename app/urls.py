from aiohttp import web

from app.views import MainView, JsForNone, APIEndpoint

url_list = [
        web.view("/", MainView),
        web.view("/plot.js", JsForNone),
        web.view("/api_endpoint", APIEndpoint),
    ]