import json
import os
from random import randint, random
from functools import lru_cache

import numpy as np

import pandas as pd

# Bokeh libraries
from bokeh.embed import autoload_static
from bokeh.models import Span, Scale, FixedTicker, LinearColorMapper, ColorBar, BasicTicker, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.resources import INLINE

from app.settings import PORT, DOMAIN, PROTOCOL, SOURCES_FILE_PATH
from bokeh.sampledata.unemployment1948 import data


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
                 tools=TOOLS,
                 tooltips=[('someTitle', 'Some information'), ('rate', '@rate')])

    fig.rect(x='level_0',
             y='level_1', width=1, height=1,
             source=df,
             fill_color={'field': 'rate', 'transform': mapper},
             line_color=None)

    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="5pt",
                         ticker=BasicTicker(desired_num_ticks=len(colors)),
                         formatter=PrintfTickFormatter(format="%d%%"),
                         label_standoff=6, border_line_color=None, location=(0, 0))
    fig.add_layout(color_bar, 'right')

    return fig


def live_render_plot():

    fig = get_total_infected_people_figure()

    js, tag = autoload_static(fig, INLINE, f"{PROTOCOL}://{DOMAIN}:{PORT}/plot.js")

    return tag, js
