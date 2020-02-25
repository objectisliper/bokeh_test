import json
import time

import aiohttp_jinja2
from aiohttp import web

from .utils import live_render_plot, get_slider, live_render_plot_update_example


@aiohttp_jinja2.template('example_html_template.html')
class MainView(web.View):
    async def get(self):
        html, js = live_render_plot()

        slider_html, slider_js = get_slider()
        return {'embed_bokeh_html': html, 'embed_js': js, 'slider_js': slider_js, 'slider_html': slider_html,
                'is_live_render': False}


class JsForNone(web.View):
    async def get(self):
        return web.Response(text='kek')


class APIEndpoint(web.View):
    async def post(self):
        html, js = live_render_plot_update_example()
        return web.Response(body=json.dumps({'html': html, 'js': js}), content_type='json')
