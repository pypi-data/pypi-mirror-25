"""
Graphing Utility Function
"""

import logging
import datetime

__author__ = 'Stephen Brown (Little Fish Solutions LTD)'

log = logging.getLogger(__name__)


def fill_missing_days(data, empty_row=None, fill_to_today=False):
    """
    Data must be a list of lists (or tuples) where the first cell in each row is a datetime which represents a month.
    The data must be ordered by the first column,

    This will return a new list of lists, with empty data added for each missing month

    :param data: The data set
    :param empty_row: Optional, list of values for all columns except the first to use for missing rows.
    :param fill_to_today: Optional, if set to True will add empty months to the end of the list up until this month
    """
    if not data:
        return data

    def find_row(date):
        for row in data:
            if row[0].date() == date:
                return row
        return None

    if not empty_row:
        empty_row = []
        for i in range(len(data[0]) - 1):
            empty_row.append(None)
    else:
        empty_row = [x for x in empty_row]

    start_date = data[0][0].date()
    end_date = data[-1][0].date()
    if fill_to_today:
        end_date = datetime.date.today()

    log.debug('Filling for date range %s - %s' % (start_date, end_date))

    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)

        current_date += datetime.timedelta(days=1)

    out = []
    for date in dates:
        existing_row = find_row(date)
        if existing_row:
            out.append(existing_row)
        else:
            out.append([datetime.datetime(date.year, date.month, date.day)] + empty_row)

    return out


def fill_missing_weeks(data, empty_row=None, fill_to_today=False):
    """
    Data must be a list of lists (or tuples) where the first cell in each row is a datetime which represents a month.
    The data must be ordered by the first column,

    This will return a new list of lists, with empty data added for each missing month

    :param data: The data set
    :param empty_row: Optional, list of values for all columns except the first to use for missing rows.
    :param fill_to_today: Optional, if set to True will add empty months to the end of the list up until this month
    """
    if not data:
        return data

    def find_row(date):
        for row in data:
            if row[0].date() == date:
                return row
        return None

    if not empty_row:
        empty_row = []
        for i in range(len(data[0]) - 1):
            empty_row.append(None)
    else:
        empty_row = [x for x in empty_row]

    start_date = data[0][0].date()
    end_date = data[-1][0].date()
    if fill_to_today:
        end_date = datetime.date.today()

    log.debug('Filling for date range %s - %s' % (start_date, end_date))

    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)

        current_date += datetime.timedelta(days=7)

    out = []
    for date in dates:
        existing_row = find_row(date)
        if existing_row:
            out.append(existing_row)
        else:
            out.append([datetime.datetime(date.year, date.month, date.day)] + empty_row)

    return out


def fill_missing_months(data, empty_row=None, fill_to_today=False):
    """
    Data must be a list of lists (or tuples) where the first cell in each row is a datetime which represents a month.
    The data must be ordered by the first column,

    This will return a new list of lists, with empty data added for each missing month

    :param data: The data set
    :param empty_row: Optional, list of values for all columns except the first to use for missing rows.
    :param fill_to_today: Optional, if set to True will add empty months to the end of the list up until this month
    """
    if not data:
        return data

    def find_row(date):
        for row in data:
            if row[0].date() == date:
                return row
        return None

    if not empty_row:
        empty_row = []
        for i in range(len(data[0]) - 1):
            empty_row.append(None)
    else:
        empty_row = [x for x in empty_row]

    start_date = data[0][0].date()
    end_date = data[-1][0].date()
    if fill_to_today:
        today = datetime.date.today()
        end_date = datetime.date(today.year, today.month, 1)

    log.debug('Filling for date range %s - %s' % (start_date, end_date))

    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        if current_date.month == 12:
            current_date = datetime.date(current_date.year + 1, 1, 1)
        else:
            current_date = datetime.date(current_date.year, current_date.month + 1, 1)

    out = []
    for date in dates:
        existing_row = find_row(date)
        if existing_row:
            out.append(existing_row)
        else:
            out.append([datetime.datetime(date.year, date.month, date.day)] + empty_row)

    return out
