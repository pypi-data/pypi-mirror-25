"""
Contains code for generating SVG line graphs
"""

import logging
import math
import decimal

import easysvg

__author__ = 'Stephen Brown (Little Fish Solutions LTD)'

log = logging.getLogger(__name__)


class SvgLineGraphStyle(object):
    def __init__(self,
                 grid_line_colour='#bbb',
                 grid_line_minor_colour='#e0e0e0',
                 axis_line_colour='#333',
                 scale_text_colour='#555',
                 scale_text_size=12,
                 y_scale_text_distance=7,
                 y_scale_text_width=50,
                 x_scale_text_height=30,
                 y_scale_text_anchor='end',
                 x_scale_border=False,
                 x_label_rotation=0,
                 show_key=True,
                 key_row_height=34,
                 key_title='Key:',
                 key_title_text_colour='#555',
                 key_title_text_size=12,
                 key_title_width=150,
                 key_label_text_colour='#555',
                 key_label_text_size=12,
                 key_max_rows=1,
                 key_order_in_columns=False,
                 auto_format_y_axis=True,
                 y_label_units=None,
                 y_label_pre_units=None,
                 y_interval=None,
                 y_minor_interval=None,
                 show_minor_x_grid_lines=True,
                 show_minor_y_grid_lines=True,
                 top_margin=10,
                 right_margin=4,
                 bottom_margin=4,
                 left_margin=4,
                 y_min_intervals=None,
                 start_y_from_zero=False,
                 x_scale_offset=1,
                 event_label_text_colour='#555',
                 event_label_text_height=10,
                 event_label_text_size=12,
                 event_label_text_rotation=0,
                 event_default_colour='#5555ff',
                 event_line_thickness=1,
                 event_triangle_size=3):
        """
        Style options for line graph

        :param grid_line_colour: Colour of majour grid lines
        :param grid_line_minor_colour: Colour of minor grid lines
        :param axis_line_colour: Colour of x and y axis
        :param scale_text_colour: Colour of text on scale on axes
        :param scale_text_size: Font size of scale text
        :param y_scale_text_distance: Horizontal distance of scale text from y axis
        :param y_scale_text_width: Width of labels on y axis
        :param x_scale_text_height: Height of x axis labels
        :param y_scale_text_anchor: SVG anchor type of y axis labels
        :param x_scale_border: Whether or not to draw a border around the x scale
        :param x_label_rotation: Degrees (clockwise) to rotate x axis labels
        :param show_key: Whether or not to show the key
        :param key_row_height: Height of a row of labels in the key section
        :param key_title: Title for key section
        :param key_title_text_colour: Colour of key title
        :param key_title_text_size: Font size of key title
        :param key_title_width: Width allowed for key title
        :param key_label_text_colour: Colour of key labels
        :param key_label_text_size: Font size of key labels
        :param key_max_rows: Maximum number of rows to display the key in
        :param key_order_in_columns: Set to True to order keys in columns instead of rows
        :param auto_format_y_axis: Whether or not to automatically format the numbers on the y
                                   axis (i.e. turning 1400 into 1.4k)
        :param y_label_units: Units to append to y axis labels
        :param y_label_pre_units: Units to prepend to y axis labels (i.e. for currencies)
        :param y_interval: Hard coded major y interval, or None for automatic
        :param y_minor_interval: Hard coded minor y interval. Must exactly divide major interval
        :param show_minor_x_grid_lines: Whether or not to show minor x grid lines
        :param show_minor_y_grid_lines: Whether or not to show minot y grid lines
        :param top_margin: Top margin size
        :param right_margin: Right margin size
        :param bottom_margin: Bottom margin size
        :param left_margin: Left margin size
        :param y_min_intervals: Minimum number of intervals on y axis
        :param start_y_from_zero: Whether or not to always start the y axis from 0
        :param x_scale_offset: Amount of pixels downwards to shift x labels
        :param event_label_text_colour: Colour of event labels, if there are events
        :param event_label_text_height: Height of event labels section, if there are events
        :param event_label_text_size: Font size of event labels
        :param event_label_text_rotation: Degrees (anti-clockwise) to rotate event labels
        :param event_default_colour: Default line colour for events
        :param event_line_thickness: Line thickness for events
        :param event_triangle_size: Triangle size at top of events. Set to 0 to disable
        """
        self.grid_line_colour = grid_line_colour
        self.grid_line_minor_colour = grid_line_minor_colour
        self.axis_line_colour = axis_line_colour
        self.scale_text_colour = scale_text_colour
        self.scale_text_size = scale_text_size
        self.y_scale_text_distance = y_scale_text_distance
        self.y_scale_text_width = y_scale_text_width
        self.x_scale_text_height = x_scale_text_height
        self.y_scale_text_anchor = y_scale_text_anchor
        self.x_scale_border = x_scale_border
        self.x_label_rotation = x_label_rotation
        self.show_key = show_key
        self.key_row_height = key_row_height
        self.key_title = key_title
        self.key_title_text_colour = key_title_text_colour
        self.key_title_text_size = key_title_text_size
        self.key_title_width = key_title_width
        self.key_label_text_colour = key_label_text_colour
        self.key_label_text_size = key_label_text_size
        self.key_max_rows = key_max_rows
        self.auto_format_y_axis = auto_format_y_axis
        self.y_label_units = y_label_units
        self.y_label_pre_units = y_label_pre_units
        self.show_minor_x_grid_lines = show_minor_x_grid_lines
        self.right_margin = right_margin
        self.top_margin = top_margin
        self.left_margin = left_margin
        self.bottom_margin = bottom_margin
        self.y_interval = y_interval
        self.y_minor_interval = y_minor_interval
        self.y_min_intervals = y_min_intervals
        self.start_y_from_zero = start_y_from_zero
        self.show_minor_y_grid_lines = show_minor_y_grid_lines
        self.key_order_in_columns = key_order_in_columns
        self.x_scale_offset = x_scale_offset
        self.event_label_text_colour = event_label_text_colour
        self.event_label_text_height = event_label_text_height
        self.event_label_text_size = event_label_text_size
        self.event_label_text_rotation = event_label_text_rotation
        self.event_default_colour = event_default_colour
        self.event_line_thickness = event_line_thickness
        self.event_triangle_size = event_triangle_size


class SvgLineGraphSeriesStyle(object):
    def __init__(self, line_colour, point_fill_colour=None, point_outline_colour=None, line_thickness=1,
                 point_outline_thickness=1, show_points=False, show_line=True, point_radius=5, shade_under_line=False,
                 shade_colour=None, key_shape='square', key_colour=None):
        """
        :param line_colour: The colour of the line
        :param point_fill_colour: The fill colour of the circles rendered for each point
        :param point_outline_colour: The outline colour of the circles rendered for each point
        :param line_thickness: The line thickness
        :param point_outline_thickness: The thickness of the outline of the circles rendered for each point
        :param show_points: Whether or not to show the points
        :param show_line: Whether or not to show the line
        :param point_radius: The radius of the circles rendered for each point
        :param shade_under_line: Whether or not to shade the area under the line
        :param shade_colour: The colour to shade the area under the line (hint: make this semi-transparent)
        :param key_shape: The shape of the key, either "square" or "circle"
        :param key_colour: The colour for the key. If None, defaults to line colour
        """
        self.line_colour = line_colour
        self.line_thickness = line_thickness
        self.point_fill_colour = point_fill_colour
        self.point_outline_colour = point_outline_colour
        self.point_outline_thickness = point_outline_thickness
        self.show_points = show_points
        self.show_line = show_line
        self.point_radius = point_radius
        self.shade_under_line = shade_under_line
        self.shade_colour = shade_colour
        self.key_shape = key_shape
        self.key_colour = key_colour

    def clone(self, line_colour=None, point_fill_colour=None, point_outline_colour=None, line_thickness=None,
              point_outline_thickness=None, show_points=None, show_line=None, point_radius=None, shade_under_line=None,
              shade_colour=None, key_shape=None, key_colour=None):
        if line_colour is None:
            line_colour = self.line_colour
        if point_fill_colour is None:
            point_fill_colour = self.point_fill_colour
        if point_outline_colour is None:
            point_outline_colour = self.point_outline_colour
        if line_thickness is None:
            line_thickness = self.line_thickness
        if point_outline_thickness is None:
            point_outline_thickness = self.point_outline_thickness
        if show_points is None:
            show_points = self.show_points
        if show_line is None:
            show_line = self.show_line
        if point_radius is None:
            point_radius = self.point_radius
        if shade_under_line is None:
            shade_under_line = self.shade_under_line
        if shade_colour is None:
            shade_colour = self.shade_colour
        if key_shape is None:
            key_shape = self.key_shape
        if key_colour is None:
            key_colour = self.key_colour

        return SvgLineGraphSeriesStyle(
            line_colour=line_colour,
            point_fill_colour=point_fill_colour,
            point_outline_colour=point_outline_colour,
            line_thickness=line_thickness,
            point_outline_thickness=point_outline_thickness,
            show_points=show_points,
            show_line=show_line,
            point_radius=point_radius,
            shade_under_line=shade_under_line,
            shade_colour=shade_colour,
            key_shape=key_shape,
            key_colour=key_colour
        )


class SvgLineGraphSeries(object):
    def __init__(self, name, data, style):
        self.name = name
        self.data = data
        self.style = style

    @property
    def num_points(self):
        return len(self.data)

    @property
    def has_data(self):
        return self.num_points > 0

    def get_rolling_average(self, average_width=10):
        """
        Return the data points for a rolling average of this series

        :param average_width: The width of the rolling average
        :return: List of numeric values, ready to add in another series
        """
        out = []
        before = average_width // 2
        
        for i in range(before):
            out.append(None)

        for i in range(len(self.data) - average_width + 1):
            total = 0
            for j in range(i, i + average_width):
                total += self.data[j]

            out.append(total / average_width)

        return out


class SvgLineGraphEvent(object):
    """
    Represents an "event" that occured at a specific x axis point.  This will be displayed as a
    labelled vertical line
    """
    def __init__(self, x_position, name, colour=None):
        """
        :param x_position: The integer position of the event, with 0 being the first x interval,
                           1 being the second...
        :param name: Even name for label
        :param colour: Colour override.  If no colour is specified, the even colour from the
                       graph style will be used instead
        """
        self.x_position = x_position
        self.name = name
        self.colour = colour


class SvgLineGraph(object):
    def __init__(self, x_labels=None, style=None, dump_debug_info=False):
        self.x_labels = x_labels
        # List of all series in the graph
        self.series = []
        # Range of y values
        self.y_min = None
        self.y_max = None
        # Number of data points
        self.x_range = 0
        if x_labels:
            self.x_range = len(x_labels)

        self.style = style if style else SvgLineGraphStyle()
        
        self.dump_debug_info = dump_debug_info

        # List of events
        self.events = {}

    def _add_series(self, series):
        self.series.append(series)

        for y in series.data:
            if y is None:
                continue
            if self.y_min is None or y < self.y_min:
                self.y_min = y

            if self.y_max is None or y > self.y_max:
                self.y_max = y

        x_range = len(series.data)
        if x_range > self.x_range:
            self.x_range = x_range

    def add_series(self, name, series_data, series_style):
        """
        Add a series to the graph

        :param series_data: A list of data points (must be numeric)
        :return: The series
        """
        series = SvgLineGraphSeries(name, series_data, series_style)

        self._add_series(series)

        return series

    def add(self, item):
        if isinstance(item, SvgLineGraphSeries):
            self._add_series(item)
        elif isinstance(item, SvgLineGraphEvent):
            self.events[item.x_position] = item
        else:
            raise ValueError('I don\'t know how to add a {}'.format(item.__class__.__name__))

    def add_event(self, x_position, name, colour=None):
        """
        Note: only one event can exist at a given x_position - subsequent events will overwrite
        existing events at a given location

        :param x_position: The integer position of the event, with 0 being the first x interval,
                           1 being the second...
        :param name: Even name for label
        :param colour: Colour override.  If no colour is specified, the even colour from the
                       graph style will be used instead
        """
        self.events[x_position] = SvgLineGraphEvent(x_position, name, colour)

    def get_default_y_interval(self):
        """
        :return: A sensible (math) interval for the y coord
        """
        # Calculate a sensible y_interval
        delta_y = self.y_max - self.y_min
        # Aim for about 10 divisions
        target = int(delta_y / 10)
        if target < 1:
            log.warn('Not supported: y_intervals < 0. Defaulting to 1')
            return 1
        else:
            num_digits = len(str(target))
            exp = num_digits - 1
            if target <= 10 ** exp:
                return 10 ** exp
            elif target <= 2 * 10 ** exp:
                return 2 * 10 ** exp
            elif target <= 5 * 10 ** exp:
                return 5 * 10 ** exp
            else:
                return 10 ** (exp + 1)

    def render(self, width, height, view_box_mode=False, dump_debug_info=None):
        """
        :return: String containing SVG render of line graph
        """
        if dump_debug_info is None:
            dump_debug_info = self.dump_debug_info

        def debug_out(text):
            if dump_debug_info:
                print(' << GRAPH DEBUG >> ' + text)

        style = self.style

        svg = easysvg.SvgGenerator()
        svg.begin(width, height, view_box_mode=view_box_mode)

        y_label_width = style.y_scale_text_width
        x_label_height = style.x_scale_text_height
        key_row_height = style.key_row_height
        if style.show_key:
            # Calculate the number of actual rows to display in the key, avoiding having less
            # than 2 items in the majority of rows
            key_num_rows = math.ceil(len(self.series) / 2)
            if key_num_rows > style.key_max_rows:
                key_num_rows = style.key_max_rows
        else:
            key_num_rows = 0
        
        key_height = key_row_height * key_num_rows
        events_height = 0
        if self.events:
            events_height = style.event_label_text_height

        left_margin = y_label_width + style.left_margin
        right_margin = style.right_margin
        top_margin = style.scale_text_size / 2 + style.top_margin + events_height
        bottom_margin = x_label_height + key_height + style.bottom_margin

        x_plot_size = width - left_margin - right_margin
        y_plot_size = height - top_margin - bottom_margin
        
        debug_out('Y Label Width: {}'.format(y_label_width))
        debug_out('X Label Height: {}'.format(x_label_height))
        debug_out('Key Row Height: {}'.format(key_row_height))
        debug_out('Key Num Rows: {}'.format(key_num_rows))
        debug_out('Key Height: {}'.format(key_height))
        debug_out('Margins (t/r/b/l): {} {} {} {}'.format(top_margin, right_margin,
                                                          bottom_margin, left_margin))
        debug_out('Plot Size: {} x {}'.format(x_plot_size, y_plot_size))

        has_data = False
        for series in self.series:
            if series.has_data:
                has_data = True
                break

        if not has_data:
            svg.rect(left_margin, top_margin, x_plot_size, y_plot_size, stroke='#aaa', fill='transparent')
            svg.text('(no data to display)', left_margin + x_plot_size / 2, top_margin + y_plot_size / 2,
                     anchor='middle', alignment_baseline='middle',
                     fill='#999')
            svg.end()
            return svg.get_svg()

        # Calculate scales etc for x coords
        x_math_offset = 0
        x_math_range = self.x_range - 1
        x_math_interval = 1

        x_steps = x_math_range - x_math_offset
        if x_steps == 0:
            x_steps = 1

        x_screen_offset = left_margin
        x_screen_range = x_plot_size
        x_screen_interval = float(x_screen_range) / x_steps
        
        # Calculate the y interval (major gridlines)
        y_math_interval = style.y_interval if style.y_interval else self.get_default_y_interval()

        # Calculate the range of values that we want to show the graph over
        y_range_min = math.floor(self.y_min / y_math_interval)
        y_range_max = math.ceil(self.y_max / y_math_interval)

        if self.style.start_y_from_zero:
            # Fudge the range to include y = 0
            if y_range_min > 0:
                y_range_min = 0
            elif y_range_max < 0:
                y_range_max = 0

        y_range = y_range_max - y_range_min

        # This allows us to set a minimum number of y intervals to display
        if style.y_min_intervals and y_range < style.y_min_intervals:
            target_range = style.y_min_intervals
            # We want to add half of the additional range above and below the current range
            # unless the additional range is odd, then we should add slightly more below it
            extra_range = target_range - y_range
            add_above = extra_range // 2
            add_below = extra_range - add_above
            # We don't want this "fudging" of the range to go over an axis
            if y_range_min >= 0 and y_range_min - add_below < 0:
                # This would cross the axis. Simply move the bottom of the range down to
                # 0 and add the additional range to the top
                add_below = y_range_min
                add_above = extra_range - add_below

            y_range_min -= add_below
            y_range_max += add_above
            y_range = y_range_max - y_range_min
        
        y_math_min = y_range_min * y_math_interval
        y_math_max = y_range_max * y_math_interval
        y_math_range = y_range * y_math_interval

        if y_math_range == 0:
            y_math_min -= y_math_interval
            y_math_max += y_math_interval
            y_math_range = y_math_max - y_math_min

        # Calculate scales etc for y coords
        y_math_offset = y_math_min  # math.floor(self.y_min / y_math_interval) * y_math_interval
        y_steps = int(y_math_range / y_math_interval)

        y_screen_offset = bottom_margin
        y_screen_range = y_plot_size
        y_screen_interval = y_screen_range / y_steps
        
        def x_math_to_screen(math_x):
            """
            Convert mathematical x coord to screen x coord
            """
            return x_screen_offset + (math_x - x_math_offset) * x_screen_interval

        def y_math_to_screen(math_y):
            """
            Convert mathematical y coord to screen x coord
            """
            return height - y_screen_offset - ((math_y - y_math_offset) / y_math_interval) * y_screen_interval

        # Draw the grid
        x_screen_min = x_math_to_screen(x_math_offset)
        x_screen_max = x_math_to_screen(x_math_offset + x_math_range)
        # Handle degenerate case!
        if x_screen_max == x_screen_min:
            x_screen_max = x_math_to_screen(x_math_offset + 1)

        y_screen_min = y_math_to_screen(y_math_offset)
        y_screen_max = y_math_to_screen(y_math_offset + y_math_range)
        
        debug_out('~~ X ~~~~~~~~~~~~~~~~~~~~~~~~~')
        debug_out('X Math Offset: {}'.format(x_math_offset))
        debug_out('X Math Range: {}'.format(x_math_range))
        debug_out('X Math Interval: {}'.format(x_math_interval))
        debug_out('X Steps: {}'.format(x_steps))
        debug_out('X Screen Offset: {}'.format(x_screen_offset))
        debug_out('X Screen Range: {}'.format(x_screen_range))
        debug_out('X Screen Interval: {}'.format(x_screen_interval))
        debug_out('X Screen Min: {}'.format(x_screen_min))
        debug_out('X Screen Max: {}'.format(x_screen_max))
        
        debug_out('~~ Y ~~~~~~~~~~~~~~~~~~~~~~~~~')
        debug_out('Y Math Offset: {}'.format(y_math_offset))
        debug_out('Y Math Range: {}'.format(y_math_range))
        debug_out('Y Math Interval: {}'.format(y_math_interval))
        debug_out('Y Steps: {}'.format(y_steps))
        debug_out('Y Screen Offset: {}'.format(y_screen_offset))
        debug_out('Y Screen Range: {}'.format(y_screen_range))
        debug_out('Y Screen Interval: {}'.format(y_screen_interval))
        debug_out('Y Screen Min: {}'.format(y_screen_min))
        debug_out('Y Screen Max: {}'.format(y_screen_max))
        
        # Draw the x grid lines (but not the y-axis to avoid layering issues)
        if x_steps > 1:
            for x_step in range(1, x_steps + 1):
                if style.show_minor_x_grid_lines or self.x_labels[x_step]:
                    screen_x = x_math_to_screen(x_step)
                    if self.x_labels[x_step]:
                        colour = style.grid_line_colour
                    else:
                        colour = style.grid_line_minor_colour

                    svg.line(screen_x, y_screen_min, screen_x, y_screen_max, stroke=colour)

        if x_steps == 1:
            # Add an extra line down the middle
            svg.line(x_screen_min + x_plot_size / 2, y_screen_min,
                     x_screen_min + x_plot_size / 2, y_screen_min - y_plot_size,
                     stroke=style.grid_line_colour)
        
        # Figure out where to draw the x axis
        math_x_axis = y_range_min
        if y_math_min < 0 and y_math_max > 0:
            math_x_axis = 0
        
        # Draw y major gridlines and x axis
        for y_step in range(y_steps + 1):
            math_y = y_step * y_math_interval + y_math_offset
            screen_y = y_math_to_screen(math_y)
            colour = style.axis_line_colour if math_y == math_x_axis else style.grid_line_colour
            svg.line(x_screen_min, screen_y, x_screen_max, screen_y, stroke=colour)
        
        # Draw y minor gridlines
        if style.y_minor_interval and style.show_minor_y_grid_lines:
            # First sanity check
            sub_divisions = y_math_interval / style.y_minor_interval
            if math.floor(sub_divisions) != sub_divisions:
                log.error('Invalid minor interval ({}) for major interval({})'
                          .format(style.y_minor_interval, y_math_interval))
            else:
                # Draw on the minor grid lines
                math_y = y_math_min
                while math_y < y_math_max:
                    if math_y % y_math_interval == 0:
                        # Already a gridline here
                        pass
                    else:
                        screen_y = y_math_to_screen(float(math_y))
                        colour = style.grid_line_minor_colour
                        svg.line(x_screen_min, screen_y, x_screen_max, screen_y, stroke=colour)

                    math_y += style.y_minor_interval

        # Draw the y axis
        y_axis = x_math_to_screen(0)
        svg.line(y_axis, y_screen_min, y_axis, y_screen_max, stroke=style.axis_line_colour)

        # Scale
        for y_step in range(y_steps + 1):
            math_y = y_step * y_math_interval + y_math_offset
            screen_y = y_math_to_screen(math_y)
            y_value = decimal.Decimal(int(y_math_offset + y_step * y_math_interval))

            if style.auto_format_y_axis:
                if y_value >= 1000000:
                    y_label = '%sm' % (y_value / 1000000)
                elif y_value >= 1000:
                    y_label = '%sk' % (y_value / 1000)
                else:
                    y_label = str(y_value)
            else:
                y_label = str(y_value)

            y_label = '%s%s%s' % (style.y_label_pre_units if style.y_label_pre_units else '',
                                  y_label,
                                  style.y_label_units if style.y_label_units else '')

            svg.text(y_label, x_screen_offset - style.y_scale_text_distance,
                     screen_y, anchor=style.y_scale_text_anchor, font_size=style.scale_text_size,
                     fill=style.scale_text_colour, alignment_baseline='middle')

        if x_steps == 1:
            svg.text(self.x_labels[0], x_screen_min + x_screen_range / 2,
                     y_screen_min + style.x_scale_text_height / 2 + 1,
                     anchor='middle', font_size=style.scale_text_size,
                     fill=style.scale_text_colour, alignment_baseline='middle')
        else:
            for x_step in range(x_steps + 1):
                if style.x_scale_border and x_step == 0:
                    continue

                if style.x_scale_border and x_step == x_steps:
                    continue

                if not self.x_labels[x_step]:
                    continue

                screen_x = x_math_to_screen(x_step)

                if style.x_label_rotation:
                    screen_y = y_screen_min + style.scale_text_size / 3 + style.x_scale_offset
                    anchor = 'start'
                    transform = easysvg.rotation_transform(style.x_label_rotation, screen_x, screen_y)
                else:
                    screen_y = y_screen_min + style.x_scale_text_height / 2 + 1
                    transform = None
                    if x_step == x_steps and not style.x_label_rotation:
                        anchor = 'end'
                    else:
                        anchor = 'middle'

                if x_step < len(self.x_labels):
                    svg.text(self.x_labels[x_step], screen_x,
                             screen_y, anchor=anchor, font_size=style.scale_text_size,
                             fill=style.scale_text_colour, alignment_baseline='middle',
                             transform=transform)

        # Border around scale
        if style.x_scale_border:
            svg.line(x_screen_min, y_screen_min, x_screen_min, y_screen_min + style.x_scale_text_height, stroke=style.grid_line_colour)
            svg.line(x_screen_max, y_screen_min, x_screen_max, y_screen_min + style.x_scale_text_height, stroke=style.grid_line_colour)
            svg.line(x_screen_min, y_screen_min + style.x_scale_text_height, x_screen_max, y_screen_min + style.x_scale_text_height, stroke=style.grid_line_colour)

        # Draw the key
        if style.show_key:
            row_length = math.ceil(len(self.series) / key_num_rows)

            key_x_offset = style.key_title_width + style.left_margin
            key_y_offset = height - key_height - style.bottom_margin
            key_width = width - right_margin - key_x_offset
            key_item_width = key_width / row_length
            key_square_offset = 10
            key_square_size = style.key_row_height - key_square_offset * 2

            svg.text(style.key_title, x_screen_min, key_y_offset + style.key_row_height / 2 + 1,
                     fill=style.key_title_text_colour, font_size=style.key_title_text_size, alignment_baseline='middle')

            i = 0
            for series in self.series:
                if style.key_order_in_columns:
                    # Keys fill columns before rows, difficult to explain I guess..
                    # Row index, 0 being top
                    row = i % key_num_rows
                    # Position in row with 0 being first (left-most)
                    row_pos = i // key_num_rows
                else:
                    # Row index, 0 being top
                    row = i // row_length
                    # Position in row with 0 being first (left-most)
                    row_pos = i % row_length
                
                row_y_offset = key_y_offset + row * style.key_row_height

                x = key_x_offset + row_pos * key_item_width
                y = row_y_offset + key_square_offset

                colour = series.style.key_colour if series.style.key_colour else series.style.line_colour
                shape = series.style.key_shape
                
                if shape == 'square':
                    svg.rect(x, y, key_square_size, key_square_size, fill=colour)
                elif shape == 'circle':
                    r = key_square_size / 2
                    svg.circle(x + r, y + r, r, fill=colour)
                else:
                    raise Exception('Invalid key shape: {}'.shape)

                svg.text(series.name, x + key_square_size + key_square_offset,
                         row_y_offset + style.key_row_height / 2 + 1,
                         alignment_baseline='middle', font_size=style.key_label_text_size,
                         fill=style.key_label_text_colour)
                i += 1
        
        # Events
        event_positions = sorted(self.events.keys())
        for event_position in event_positions:
            event = self.events[event_position]
            math_x = event_position * x_math_interval
            screen_x = x_math_to_screen(math_x)
            top = y_screen_max
            bottom = y_screen_min
            triangle_size = style.event_triangle_size

            if triangle_size:
                top += style.event_triangle_size

            event_colour = event.colour
            if event_colour is None:
                event_colour = style.event_default_colour
            
            # Vertical Line
            svg.line(screen_x, bottom, screen_x, top, stroke=event_colour,
                     stroke_width=style.event_line_thickness)
            
            # Triangle
            if triangle_size:
                svg.polygon([
                    (screen_x - triangle_size, top - triangle_size),
                    (screen_x + triangle_size, top - triangle_size),
                    (screen_x, top)
                ], stroke=event_colour, fill=event_colour)
            
            # Label
            anchor = 'middle'
            label_y = top - style.event_label_text_size / 2 - 1
            transform = None

            if style.event_label_text_rotation:
                anchor = 'start'
                transform = easysvg.rotation_transform(-style.event_label_text_rotation, screen_x,
                                                       label_y)

            svg.text(event.name, screen_x, label_y, anchor=anchor, transform=transform,
                     font_size=style.event_label_text_size, fill=style.event_label_text_colour)

        # Calculate screen coordinates for each of the series
        for series in self.series:
            # Create a list of points
            series._screen_points = []

            for i in range(series.num_points):
                math_x = i * x_math_interval
                math_y = series.data[i]

                if math_y is None:
                    continue

                screen_x = x_math_to_screen(math_x)
                screen_y = y_math_to_screen(math_y)

                series._screen_points.append((screen_x, screen_y))

        if x_steps == 1:
            # Degenerate case - 1 point!
            # Shade under lines
            for series in self.series:
                if series.style.shade_under_line:
                    points = [
                        (x_screen_min, y_screen_min),
                        (x_screen_min, series._screen_points[0][1]),
                        (x_screen_max, series._screen_points[0][1]),
                        (x_screen_max, y_screen_min)
                    ]

                    svg.polygon(points, fill=series.style.shade_colour)

            # Plot the lines
            for series in self.series:
                if series.style.show_line:
                    x1, y1 = x_screen_min, series._screen_points[0][1]
                    x2, y2 = x_screen_min + x_plot_size, series._screen_points[0][1]

                    svg.line(x1, y1, x2, y2, stroke=series.style.line_colour,
                             stroke_width=series.style.line_thickness)

            # Plot the points
            for series in self.series:
                if series.style.show_points:
                    x, y = series._screen_points[0]
                    svg.circle(x_screen_min + x_plot_size / 2, y, series.style.point_radius, series.style.point_outline_colour,
                               series.style.point_fill_colour, series.style.point_outline_thickness)

        else:
            # Normal conditions - draw a proper line graph
            # Shade under lines
            for series in self.series:
                if series.style.shade_under_line:
                    p_first = (series._screen_points[0][0], y_screen_min)
                    p_last = (series._screen_points[-1][0], y_screen_min)

                    svg.polygon([p_first] + series._screen_points + [p_last], fill=series.style.shade_colour)

            # Plot the lines
            for series in self.series:
                if series.style.show_line:
                    for i in range(len(series._screen_points) - 1):
                        x1, y1 = series._screen_points[i]
                        x2, y2 = series._screen_points[i + 1]

                        svg.line(x1, y1, x2, y2, stroke=series.style.line_colour,
                                 stroke_width=series.style.line_thickness)

            # Plot the points
            for series in self.series:
                if series.style.show_points:
                    for point in series._screen_points:
                        x, y = point
                        svg.circle(x, y, series.style.point_radius, series.style.point_outline_colour,
                                   series.style.point_fill_colour, series.style.point_outline_thickness)

        svg.end()
        return svg.get_svg()
