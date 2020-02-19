import json
import os
from random import randint, random
from functools import lru_cache

import numpy as np

import pandas as pd

# Bokeh libraries
from bokeh import events
from bokeh.embed import autoload_static
from bokeh.models import Span, Scale, FixedTicker, LinearColorMapper, ColorBar, BasicTicker, PrintfTickFormatter, \
    CustomJS, ColumnDataSource, TapTool
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.sampledata.iris import flowers
from bokeh.transform import factor_mark, factor_cmap
import bokeh.models as bkm

from app.settings import PORT, DOMAIN, PROTOCOL, SOURCES_FILE_PATH
from bokeh.sampledata.unemployment1948 import data

SPECIES = ['setosa', 'versicolor', 'virginica']
MARKERS = ['hex', 'circle_x', 'triangle']


def get_total_infected_people_figure():
    with open(SOURCES_FILE_PATH) as f:
        source_data = json.load(f)

    df = pd.DataFrame(source_data['image'])

    df = pd.DataFrame(df.stack(), columns=['rate']).reset_index()

    colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
    mapper = LinearColorMapper(palette=colors, low=df.rate.min(), high=df.rate.max())

    TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

    # Create a figure with a datetime type x-axis
    fig = figure(title=source_data['name'],
                 plot_height=900, plot_width=900,
                 x_axis_label=source_data['x'], y_axis_label=source_data['y'],
                 x_minor_ticks=5, y_range=(0, 50), x_range=(0, 50), y_minor_ticks=5,
                 y_scale=Scale(),
                 toolbar_location='below',
                 tools=TOOLS, tooltips=[])

    rects = fig.rect(x='level_0',
                     y='level_1', width=1, height=1,
                     source=df,
                     fill_color={'field': 'rate', 'transform': mapper},
                     line_color=None)

    stars = fig.scatter("petal_length", "sepal_width", source=flowers, legend_field="species",
                        fill_alpha=0.4, size=12,
                        marker=factor_mark('species', MARKERS, SPECIES),
                        color=factor_cmap('species', 'Category10_3', SPECIES))

    g1_hover = bkm.HoverTool(renderers=[rects],
                             tooltips=[('rects', 'rects')])

    g2_hover = bkm.HoverTool(renderers=[stars],
                             tooltips=[('stars', 'stars')])

    fig.add_tools(g1_hover, g2_hover)

    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                         ticker=BasicTicker(desired_num_ticks=len(colors)),
                         formatter=PrintfTickFormatter(format="%d%%"),
                         label_standoff=6, border_line_color=None, location=(0, 0))

    tap_tool_1 = TapTool(behavior='inspect', callback=CustomJS(args=dict(), code=get_callback_function('red')
     ), renderers=[rects])

    tap_tool_2 = TapTool(behavior='inspect', callback=CustomJS(args=dict(), code=get_callback_function('violet')
     ), renderers=[stars])

    fig.add_tools(tap_tool_1, tap_tool_2)

    fig.add_layout(color_bar, 'right')

    return fig


def get_callback_function(color):
    return """
        const previous_element = document.getElementById("block-info");
        if (previous_element) {
            document.body.removeChild(previous_element)
        }
        var elem = document.createElement('div');
        elem.style.cssText = 'position:absolute;width:100px;height:100px;top: 10px;left:10px;background-color:%s;';
        elem.id = 'block-info';
        elem.innerHTML = cb_data.geometries['x'].toFixed(0) + " " + cb_data.geometries['y'].toFixed(0);
        document.body.appendChild(elem);
        """ % color


def live_render_plot():
    fig = get_total_infected_people_figure()

    js, tag = autoload_static(fig, INLINE, f"{PROTOCOL}://{DOMAIN}:{PORT}/plot.js")

    return tag, js
