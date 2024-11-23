import logging
import re
from collections import OrderedDict, defaultdict
from enum import Enum
from typing import Dict, Any

import requests

from core.data.models.hour_by_hour_model import HourByHourModel
logger = logging.getLogger(__name__)

class TransType(Enum):
    SMT_IN = "INPUT",
    SMT_OUT = "OUTPUT",
    PACKING = "PACKING",


# http://10.13.89.96:83/home/reporte?entrada=2024112100&salida=202411210100&transtype=INPUT
# e.g. respond
# [
#     {
#         "LINE": "00",
#         "HOURS": "0000",
#         "QTY": 416,
#         "NEXTDAY": 0
#     },
#     {
#         "LINE": "00",
#         "HOURS": "0100",
#         "QTY": 381,
#         "NEXTDAY": 0
#     },
#     {
#         "LINE": "SMTJ01A",
#         "HOURS": "0000",
#         "QTY": 99,
#         "NEXTDAY": 0
#     },
#     {
#         "LINE": "SMTJ01A",
#         "HOURS": "0100",
#         "QTY": 99,
#         "NEXTDAY": 0
#     },
#     {
#         "LINE": "SMTJ02A",
#         "HOURS": "0000",
#         "QTY": 148,
#         "NEXTDAY": 0
#     },
#     {
#         "LINE": "SMTJ02A",
#         "HOURS": "0100",
#         "QTY": 155,
#         "NEXTDAY": 0
#     },
#     {
#         "LINE": "SMTJ06",
#         "HOURS": "0000",
#         "QTY": 120,
#         "NEXTDAY": 0
#     },
#     {
#         "LINE": "SMTJ06",
#         "HOURS": "0100",
#         "QTY": 77,
#         "NEXTDAY": 0
#     },
#     {
#         "LINE": "SMTJ09A",
#         "HOURS": "0000",
#         "QTY": 49,
#         "NEXTDAY": 0
#     },
#     {
#         "LINE": "SMTJ09A",
#         "HOURS": "0100",
#         "QTY": 50,
#         "NEXTDAY": 0
#     }
# ]

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
    print(f"Fetching data from URL: {_url}")
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

def api_respond_to_model(data, date:str):
    _data = defaultdict(list)
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

            records = _data[line]
            # Find existing record for this line and hour
            existing_record = next((record for record in records if record.hour == hour), None)
            if existing_record:
                # Update the appropriate field
                setattr(existing_record, field, qty)
            else:
                # Create a new record with default values
                new_record = HourByHourModel(
                    date=date,
                    line=line,
                    hour=hour,
                    smt_in=0,
                    smt_out=0,
                    packing=0
                )
                setattr(new_record, field, qty)
                records.append(new_record)

    # Sort the _data dictionary by line keys
    sorted_data = OrderedDict(sorted(_data.items()))
    # Sort the records within each line by hour
    for records in sorted_data.values():
        records.sort(key=lambda record: record.hour)


        # **Print the result with formatting**
    # for line, records in sorted_data.items():
    #     print(f"\nLine: {line}")
    #     print(f"{'Date':<12} {'Hour':<6} {'SMT In':<8} {'SMT Out':<8} {'Packing':<8}")
    #     print("-" * 50)
    #     for record in records:
    #         print(f"{record.date:<12} {record.hour:<6} {record.smt_in:<8} {record.smt_out:<8} {record.packing:<8}")


    return sorted_data






# if __name__ == "__main__":
#     # get_all_day("20241121")
#     date = "2024-11-21"
#     # api_respond_to_model(get_all_day(transform_date_to_mackenzie(date)),date)
#     api_respond_to_model(get_hour_by_hour(transform_date_to_mackenzie(date), "01"),date)
#
#     # print(get_all_day("20241120"))
#     pass
