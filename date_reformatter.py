from datetime import datetime


def format_date(date_str):
    """

    :param date_str: a date string:
    :return: A date string without hyphens
    """
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%Y%m%d')
