import json

from core.data.dao.hbh_dao import HbhDAO, PlatformDAO, WorkPlanDAO

import requests
from datetime import datetime, timedelta
from typing import List
from concurrent.futures import ThreadPoolExecutor

from core.data.schemas.hour_by_hour_schema import HourByHourSchema, PlatformSchema, WorkPlanSchema
from core.db.database import DBConnection


def get_outputs_from_pocket_base_by_date(date: str) -> List[dict]:
    """
    Fetches output records from PocketBase for a given date.

    :param date: Date in the format "YYYY-MM-DD" (e.g., "2024-11-23").
    :return: List of records for the given date.
    """
    url = f"http://10.13.33.46:3030/api/collections/day/records?filter=(work_date%20~%20%27{date}%27)&expand=hours"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            print(f"Failed to fetch data for {date}: HTTP {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Request failed for {date}: {e}")
        return []


def process_records_for_date(date: str) -> List:
    """
    Fetch and process work hour data for a single date.

    :param date: Date for which to fetch and process data.
    :return: List of HourByHourModel objects.
    """
    records = get_outputs_from_pocket_base_by_date(date)
    work_hour_schema: List[HourByHourSchema] = []

    if records:
        for record in records:
            hours = record.get("expand", {}).get("hours", [])
            for hour in hours:
                work_hour_schema.append(HourByHourSchema(
                    factory="A6",
                    line=record.get("line"),
                    date=str(record.get("work_date"))[:10],
                    hour=hour.get("place"),
                    smt_in=hour.get("smtIn"),
                    smt_out=hour.get("smtOut"),
                    packing=hour.get("packing")
                ))

    return work_hour_schema


def get_all_dates(days: int) -> List[str]:
    """
    Generates a list of dates in the format "YYYY-MM-DD" for the past `days` days.

    :param days: Number of past days to generate dates for.
    :return: List of dates in "YYYY-MM-DD" format.
    """
    return [(datetime.now() - timedelta(days=i + 1)).strftime("%Y-%m-%d") for i in range(days)]


def get_out_form_pb_by_days(days: int) -> List[HourByHourSchema]:
    """
    Fetches and processes work hour data from PocketBase for the last `days` days in parallel.

    :param days: Number of days to fetch data for.
    :return: List of HourByHourModel objects.
    """
    dates = get_all_dates(days)
    work_hour_schema: List[HourByHourSchema] = []

    # Use ThreadPoolExecutor for multi-threading
    with ThreadPoolExecutor() as executor:
        # Map each date to a thread and collect results
        results = list(executor.map(process_records_for_date, dates))

    # Flatten the results
    for result in results:
        work_hour_schema.extend(result)

    # Print each record (for debugging or logging)
    # for item in work_hour_schema:
    #     print(item.to_dict())

    return work_hour_schema


def save_to_db(data: List[HourByHourSchema]):
    dao = HbhDAO(connection=DBConnection().get_session())

    dao.query_add_records(data)

    # for record in data:
    #     print(f"Saving record: {record}")
    # Save the record to the database


def pb_to_db(days: int):
    data = get_out_form_pb_by_days(days)
    save_to_db(data)


def pb_to_json(days: int, dir: str):
    data = get_out_form_pb_by_days(days)

    data = [record.to_dict() for record in data]

    print(f"Saving {len(data)} records to {dir}/hour_by_hour.json")
    with open(f'{dir}/hour_by_hour.json', 'w') as f:
        f.write(json.dumps(data, indent=4))


def platform_to_db_from_json(file_path: str):
    with open(file_path, 'r') as f:
        data = json.load(f)

    data = [PlatformSchema(
        id= record.get('id'),
        name=record.get('platform'),
        sku=record.get('sku'),
        uph=record.get('uph'),
        f_n=record.get('f_n')
    ) for record in data]

    if not data:
        print("No data to save")
        return

    dao = PlatformDAO(connection=DBConnection().get_session())
    dao.query_add_records(data)


def work_plan_to_db_from_json(file_path: str):
    with open(file_path, 'r') as f:
        data = json.load(f)

    data = [WorkPlanSchema(
        date=record.get('date'),
        factory="A6",
        line=record.get('line'),
        planned_hours=record.get('planed_hours'),
        platform_id=record.get('platform_id'),
        state=record.get('state'),
        target_oee=record.get('target_oee'),
        uph_i=record.get('uph_i'),
        week=record.get('week')
    ) for record in data]

    if not data:
        print("No data to save")
        return

    dao = WorkPlanDAO(connection=DBConnection().get_session())
    dao.query_add_records(data)


def hour_by_hour_to_db_from_json(file_path: str):
    with open(file_path, 'r') as f:
        data = json.load(f)

    data = [HourByHourSchema(
        factory=record.get('factory'),
        line=record.get('line'),
        date=record.get('date'),
        hour=record.get('hour'),
        smt_in=record.get('smt_in'),
        smt_out=record.get('smt_out'),
        packing=record.get('packing')
    ) for record in data]

    if not data:
        print("No data to save")
        return


    dao = HbhDAO(connection=DBConnection().get_session())
    dao.query_add_records(data)


