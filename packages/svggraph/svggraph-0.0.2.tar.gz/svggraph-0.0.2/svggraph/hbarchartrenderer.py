"""
Horizontal Bar Chart
"""

import logging
import decimal

import easysvg

__author__ = 'Stephen Brown (Little Fish Solutions LTD)'

log = logging.getLogger(__name__)


class SvgHBarChartStyle(object):
    def __init__(self, bar_background_colour='#DDD', bar_colour='#0000AA', bar_height=20, bar_spacing=15,
                 label_text_size=14, label_text_colour='#555', label_height=20, normalise=True):
        self.bar_background_colour = bar_background_colour
        self.bar_colour = bar_colour
        self.bar_height = bar_height
        self.bar_spacing = bar_spacing
        self.label_text_size = label_text_size
        self.label_text_colour = label_text_colour
        self.label_height = label_height
        self.normalise = normalise


class SvgHBarChartDataPoint(object):
    def __init__(self, name, value, ratio, ratio_to_max):
        self.name = name
        self.value = value
        self.ratio = ratio
        self.ratio_to_max = ratio_to_max


class SvgHBarChart(object):
    """
    Currently only supports a single series
    """
    def __init__(self, labels, data, style=None):
        if len(labels) != len(data):
            raise Exception('Number of labels must match number of data points')

        self.data = []

        total = decimal.Decimal(0)
        max_value = decimal.Decimal(0)

        for item in data:
            total += item
            if item > max_value:
                max_value = item

        for i in range(len(data)):
            self.data.append(SvgHBarChartDataPoint(labels[i],
                                                   decimal.Decimal(data[i]),
                                                   decimal.Decimal(data[i]) / total if total else 0,
                                                   decimal.Decimal(data[i]) / max_value if max_value else 0))

        self.style = style if style else SvgHBarChartStyle()

    def render(self, width):
        """
        :return: String containing SVG render of line graph
        """
        style = self.style
        svg = easysvg.SvgGenerator()

        margin = 5

        item_height = style.label_height + style.bar_height + style.bar_spacing
        height = item_height * len(self.data) + 2 * margin
        svg.begin(width, height)

        i = 0
        for item in self.data:
            item_offset_y = margin + item_height * i
            # Label
            svg.text(item.name, margin, item_offset_y + style.label_height / 2.0, alignment_baseline='middle',
                     font_size=style.label_text_size, fill=style.label_text_colour)
            # Percentage
            svg.text('%.0f%%' % (item.ratio * 100), width - margin, item_offset_y + style.label_height / 2.0,
                     alignment_baseline='middle', font_size=style.label_text_size, fill=style.label_text_colour,
                     anchor='end')

            # Bar
            bar_offset_y = item_offset_y + style.label_height
            max_bar_width = width - margin * 2
            svg.rect(margin, bar_offset_y, max_bar_width, style.bar_height, fill=style.bar_background_colour)
            bar_width = max_bar_width * item.ratio_to_max if style.normalise else max_bar_width * item.ratio
            svg.rect(margin, bar_offset_y, bar_width, style.bar_height,
                     fill=style.bar_colour)
            i += 1

        svg.end()
        return svg.get_svg()
