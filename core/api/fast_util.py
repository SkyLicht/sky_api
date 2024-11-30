from datetime import datetime
from fastapi import HTTPException
import re

def validate_date_range(start_date: str, end_date: str) -> tuple[datetime, datetime]:
    """
    Validates the date range and returns datetime objects for the start and end dates.

    Args:
        start_date (str): The start date in 'yyyy-mm-dd' format.
        end_date (str): The end date in 'yyyy-mm-dd' format.

    Returns:
        tuple[datetime, datetime]: The validated start and end dates as datetime objects.

    Raises:
        HTTPException: If validation fails for date format, range, or logical errors.
    """
    # Define the regex pattern for the date format yyyy-mm-dd
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"

    # Validate the format of both dates
    if not re.match(date_pattern, start_date) or not re.match(date_pattern, end_date):
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Dates must be in yyyy-mm-dd format."
        )

    # Parse the date strings into datetime objects
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        today_date_obj = datetime.now()
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error parsing dates: {e}"
        )

    # Check logical conditions for the date range
    if start_date_obj > end_date_obj:
        raise HTTPException(
            status_code=400,
            detail="Start date must be earlier than or equal to end date."
        )

    if start_date_obj > today_date_obj:
        raise HTTPException(
            status_code=400,
            detail="Start date must be earlier than or equal to today's date."
        )

    return start_date_obj, end_date_obj