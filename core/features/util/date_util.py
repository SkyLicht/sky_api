from datetime import datetime


def transform_date_to_mackenzie(date_str):
    # Parse the input string to a datetime object
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    # Format the datetime object to the desired output string
    return date_obj.strftime('%Y%m%d')