"""
Package for drawing SVG graphs
"""

import logging

from .linegraphrender import SvgLineGraph, SvgLineGraphStyle, SvgLineGraphSeriesStyle, SvgLineGraphSeries, SvgLineGraphEvent
from .piechartrenderer import SvgPieChart, SvgPieChartStyle, SvgPieChartItemStyle
from .hbarchartrenderer import SvgHBarChart, SvgHBarChartStyle

__author__ = 'Stephen Brown (Little Fish Solutions LTD)'

log = logging.getLogger(__name__)

