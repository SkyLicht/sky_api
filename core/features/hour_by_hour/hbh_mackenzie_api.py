import logging
import re
from collections import OrderedDict, defaultdict
from datetime import datetime
from enum import Enum
from typing import Dict, Any

import requests
from watchfiles import awatch

from core.data.models.hour_by_hour_model import HourByHourModel
from core.features.util.date_util import transform_date_to_mackenzie

logger = logging.getLogger(__name__)

class TransType(Enum):
    SMT_IN = "INPUT",
    SMT_OUT = "OUTPUT",
    PACKING = "PACKING",


# http://10.13.89.96:83/home/reporte?entrada=2024112100&salida=202411210100&transtype=INPUT


def url(
        start_day: str,
        end_day: str,
        start_hour: str,
        end_hour: str,
        trans_type: TransType
) -> str:
    return (
        f"http://10.13.89.96:83/home/reporte?"
        f"entrada={start_day}{start_hour}"
        f"&salida={end_day}{end_hour}00"
        f"&transtype={trans_type.value[0]}"
    )

def fetch_data(
        start_day: str,
        end_day: str,
        start_hour: str,
        end_hour: str,
        trans_type: TransType
) -> Any:
    _url = url(
        start_day=start_day,
        end_day=end_day,
        start_hour=start_hour,
        end_hour=end_hour,
        trans_type=trans_type
    )
    logger.debug(f"Fetching data from URL: {_url}")
    # print(f"Fetching data from URL: {_url}")
    try:
        response = requests.get(_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data for {trans_type.name}: {e}")
        return None  # You might choose to handle this differently

def get_transactions(
        day: str,
        start_hour: str,
        end_hour: str
) -> Dict[str, Any]:
    data = {}
    transaction_types = [
        ('smt_in', TransType.SMT_IN),
        ('smt_out', TransType.SMT_OUT),
        ('packing', TransType.PACKING)
    ]

    for key, trans_type in transaction_types:
        result = fetch_data(
            start_day=day,
            end_day=day,
            start_hour=start_hour,
            end_hour=end_hour,
            trans_type=trans_type
        )
        if result is not None:
            data[key] = result
        else:
            logger.warning(f"No data returned for {key} on {day} between {start_hour} and {end_hour}")

    return data

def get_hour_by_hour(day: str, hour: str) -> Dict[str, Any]:
    return get_transactions(day=day, start_hour=hour, end_hour=hour)

def get_all_day(day: str) -> Dict[str, Any]:
    return get_transactions(day=day, start_hour="00", end_hour="23")


async def api_respond_to_model(data, date: str):
    if not data:
        return None
    # Dictionary to store unique records with keys as "line-hour"
    unique_records = {}

    data_fields = ['smt_in', 'smt_out', 'packing']

    for field in data_fields:
        for item in data.get(field, []):
            # Extract the line identifier (e.g., 'J01')
            match = re.search(r"J\d{2}", item.get('LINE', ''))
            if not match:
                continue
            line = match.group()
            hour = item.get('HOURS', '')[:2]
            qty = item.get('QTY', 0)

            # Create a unique key for each "line-hour" combination
            key = f"{line}-{hour}"

            # Check if the record already exists
            if key in unique_records:
                # Update the existing record
                setattr(unique_records[key], field, qty)
            else:
                # Create a new record with default values
                unique_records[key] = HourByHourModel(
                    date=date,
                    line=line,
                    hour=hour,
                    smt_in=0,
                    smt_out=0,
                    packing=0
                )
                # Set the appropriate field
                setattr(unique_records[key], field, qty)

    # Sort records by line and hour

    sorted_records = OrderedDict(sorted(unique_records.items()))

    # Print the result with formatting
    #print_records(sorted_records.values())

    return sorted_records



def print_records(records):
    """
    Utility function to print formatted records.
    """
    current_line = None
    for record in records:
        if record.line != current_line:
            if current_line is not None:
                print()  # New line between lines
            current_line = record.line
            print(f"Line: {record.line}")
            print(f"{'Date':<12} {'Hour':<6} {'SMT In':<8} {'SMT Out':<8} {'Packing':<8}")
            print("-" * 50)

        print(f"{record.date:<12} {record.hour:<6} {record.smt_in:<8} {record.smt_out:<8} {record.packing:<8}")



if __name__ == "__main__":
    get_current_day = datetime.now().strftime("%Y-%m-%d")
    get_current_hour_in_string = datetime.now().strftime("%H")
    responds =  api_respond_to_model(
        get_hour_by_hour(transform_date_to_mackenzie(get_current_day), get_current_hour_in_string),
        get_current_day,
    )

    for keys, records in responds.items():
        print(records)

    pass
