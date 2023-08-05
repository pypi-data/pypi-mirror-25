"""
Renders a lovely pie chart!  Mmmmmmmmm pie...
"""

import logging
import decimal
import math

import easysvg

__author__ = 'Stephen Brown (Little Fish Solutions LTD)'

log = logging.getLogger(__name__)


class SvgPieChartStyle(object):
    def __init__(self, pie_margin=10, key_margin=10, key_item_height=30, key_font_colour='#555', key_font_size=14,
                 key_spot_radius=6):
        self.pie_margin = pie_margin
        self.key_margin = key_margin
        self.key_item_height = key_item_height
        self.key_font_colour = key_font_colour
        self.key_font_size = key_font_size
        self.key_spot_radius = key_spot_radius


class SvgPieChartItemStyle(object):
    def __init__(self, fill_colour='black'):
        self.fill_colour = fill_colour


class SvgPieChartItem(object):
    def __init__(self, name, value, style=None):
        self.name = name
        self.value = value
        self.style = style if style else SvgPieChartItemStyle()


class SvgPieChart(object):
    def __init__(self, style=None):
        self.data = []
        self.style = style if style else SvgPieChartStyle()

    def add_item(self, name, value, style=None):
        self.data.append(SvgPieChartItem(name, value, style))

    # noinspection PyProtectedMember
    def render(self, width, view_box_mode=False):
        """
        :return: String containing SVG render of line graph
        """
        style = self.style

        svg = easysvg.SvgGenerator()

        pie_margin = float(style.pie_margin)
        pie_r = width / 2.0 - pie_margin
        pie_cx = pie_r + pie_margin
        pie_cy = pie_r + pie_margin

        height = 2 * (pie_r + pie_margin) + len(self.data) * style.key_item_height + style.key_margin

        svg.begin(width, height, view_box_mode=view_box_mode)

        # First of all, calculate the total across all data items, and then work out the proportion of the pie for
        # each item
        if len(self.data) == 0:
            svg.text('(no data to display)', width / 2, height / 2,
                     anchor='middle', alignment_baseline='middle',
                     fill='#999')
            svg.end()
            return svg.get_svg()

        if len(self.data) == 1:
            # Special case, only 1 item so always 100%
            self.data[0]._ratio = 1
        else:
            total = decimal.Decimal(0)
            for item in self.data:
                total += item.value

            # We want to be 100% sure that these always add up to 100%
            non_last_total = decimal.Decimal(0)
            for i in range(len(self.data) - 1):
                item = self.data[i]
                item._ratio = item.value / total
                non_last_total += item._ratio

            self.data[-1]._ratio = decimal.Decimal(1) - non_last_total

        # Render the pie!
        if len(self.data) == 1:
            item = self.data[0]
            svg.circle(pie_cx, pie_cy, pie_r, fill=item.style.fill_colour)
        else:
            # Start of next slice in radians
            start_of_segment = decimal.Decimal(0)
            pi = decimal.Decimal(math.pi)
            for item in self.data:
                end_of_segment = start_of_segment + item._ratio * 2 * pi

                svg.arc(pie_cx, pie_cy, pie_r, start_of_segment, end_of_segment, fill=item.style.fill_colour)
                start_of_segment = end_of_segment

        # Now draw the key
        key_offset_y = 2 * (pie_r + pie_margin)
        key_offset_x = style.key_margin

        i = 0
        for item in self.data:
            item_offset_x = key_offset_x
            item_offset_y = key_offset_y + i * style.key_item_height

            cx = item_offset_x + style.key_spot_radius
            cy = item_offset_y + style.key_item_height / 2.0
            svg.circle(cx, cy, style.key_spot_radius, fill=item.style.fill_colour)
            svg.text(item.name, cx + style.key_spot_radius * 2, cy, fill=style.key_font_colour,
                     font_size=style.key_font_size, alignment_baseline='middle')
            svg.text('%.0f%%' % (item._ratio * 100), width - style.key_margin, cy, anchor='end',
                     fill=style.key_font_colour, font_size=style.key_font_size)

            i += 1

        svg.end()
        return svg.get_svg()
