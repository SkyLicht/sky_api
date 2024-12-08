from datetime import datetime, timedelta, date
from enum import Enum


class ExcelDateType(Enum):

    INTEGER = 0
    SHORT_DATE = 1
    LONG_DATE = 2

def date_get_range_from_year_and_week(year: int, week: int):
    """
    Given a year and week number, return the start and end dates of that ISO week.

    :param year: The year as an integer
    :param week: The ISO week number as an integer
    :return: A tuple with start and end dates (both inclusive)
    """
    # Get the first day of the given year
    first_day_of_year = datetime(year, 1, 1)

    # Calculate the date of the first Monday of the ISO calendar
    first_monday = first_day_of_year + timedelta(days=(7 - first_day_of_year.weekday() + 1) % 7)

    # Calculate the start date of the given week
    start_date = first_monday + timedelta(weeks=week - 1)

    # Calculate the end date (Sunday) of the given week
    end_date = start_date + timedelta(days=5)

    return start_date.date(), end_date.date()

def date_get_week_from_date_str(str_date: str) -> int:
    """
    Given a date string in the format 'YYYY-MM-DD', return the ISO week number.

    :param str_date: A date string in the format 'YYYY-MM-DD'
    :return: The ISO week number as an integer
    """
    date_obj = datetime.strptime(str_date, '%Y-%m-%d')
    return date_obj.isocalendar()[1]

def date_get_year_from_date_str(str_date: str) -> int:
    """
    Given a date string in the format 'YYYY-MM-DD', return the year as an integer.

    :param str_date: A date string in the format 'YYYY-MM-DD'
    :return: The year as an integer
    """
    date_obj = datetime.strptime(str_date, '%Y-%m-%d')
    return date_obj.year

def date_str_date_to_excel_date(date_str: str, excel_type: ExcelDateType= ExcelDateType.INTEGER) -> int | str:
    """
    Convert a date string in the format 'YYYY-MM-DD' to an Excel date.

    :param date_str: A date string in the format 'YYYY-MM-DD'
    :param excel_type: The type of Excel date to return
    """

    # Check if the date string is valid
    if not date_str:
        return "not_valid"

    date_obj = datetime.strptime(date_str, '%Y-%m-%d')

    if excel_type == ExcelDateType.INTEGER:
        return date_obj.toordinal() - datetime(1899, 12, 30).toordinal()
    elif excel_type == ExcelDateType.SHORT_DATE:
        return date_obj.strftime('%m/%d/%Y')
    elif excel_type == ExcelDateType.LONG_DATE:
        return date_obj.strftime('%A, %B %d, %Y')
    else:
        return "not_valid"

def date_str_from_date_obj(date_obj: date) -> str:
    """
    Convert a datetime object to a date string in the format 'YYYY-MM-DD'.

    :param date_obj: A datetime object
    :return: A date string in the format 'YYYY-MM-DD'
    """
    return date_obj.strftime('%Y-%m-%d')