import time

import aiohttp_jinja2
from aiohttp import web

from .utils import live_render_plot


@aiohttp_jinja2.template('example_html_template.html')
class MainView(web.View):
    async def get(self):
        html, js = live_render_plot()
        return {'embed_bokeh_html': html, 'embed_js': js,
                'is_live_render': False}


class JsForNone(web.View):
    async def get(self):
        return web.Response(text='kek')
