from datetime import datetime, timedelta


def transform_date_to_mackenzie(date_str):
    # Parse the input string to a datetime object
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    # Format the datetime object to the desired output string
    return date_obj.strftime('%Y%m%d')

def transform_range_of_dates(form: str, at: str)-> list[str]:
    # Parse the input string to a datetime object
    # And return a list of dates in the range
    # Return a list of dates (str '%Y-%m-%d') in the range
    form_date = datetime.strptime(form, '%Y-%m-%d')
    at_date = datetime.strptime(at, '%Y-%m-%d')
    date_list = []
    while form_date <= at_date:
        date_list.append(form_date.strftime('%Y-%m-%d'))
        form_date += timedelta(days=1)
    return date_list

