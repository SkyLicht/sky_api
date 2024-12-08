import json
from io import BytesIO
from typing import Optional

from openpyxl.workbook import Workbook
from requests import session

from core.api.querys.hbh_query import GetHbhQuery
from core.data.dao.hbh_dao import WorkPlanDAO, HbhDAO
from core.data.handlers.handler_hour_by_hour import handle_weekly_kpi
from core.data.handlers.translator import translate_hour_by_hour_schema_to_model, \
    translate_hour_by_hour_schema_list_to_model_list
from core.data.models.hour_by_hour_model import HourByHourModel
from core.data.models.request_model import RequestWeekEffModel
from core.db.util import scoped_execute, http_handle_error, scoped_execute_async
from core.features.hour_by_hour.hbh_service import HbhService
from core.util import date_get_range_from_year_and_week, date_str_date_to_excel_date, ExcelDateType, \
    date_str_from_date_obj


class HourByHourRepository:

    def __init__(self, db, logger=None):
        self.scoped_session = db
        self.dao = WorkPlanDAO(db)
        self.hbh_dao = HbhDAO(db)
        self.service = HbhService(dao=self.hbh_dao)
        self.logger = logger

    async def get_kpi_by_week(self, request_body: RequestWeekEffModel) -> dict | None:

        db_result = scoped_execute(
            session_factory=session,
            query_function=lambda _session: self.dao.get_work_hour_by_week(week=request_body.week),
            on_complete=lambda query_result: print(f'data fetched'),
            handle_error=http_handle_error
        )

        if db_result.data is None:
            return None

        _data = db_result.data

        ie_kpi = handle_weekly_kpi(request_body, _data)

        return ie_kpi

    async def update_previews_day(self):

        return self.service.update_previews_day()

    async def update_range_of_dates(self, start_date: str, end_date: str):

        _responds = await self.service.update_hours_form_range_of_dates(start_date, end_date)
        return _responds

    async def get_hour_by_hour_by(self, query: GetHbhQuery) -> list[HourByHourModel] :
        self.logger.info("Processing get_hour_by_hour_by request")
        # Determine date range
        start_date_str: Optional[str] = None
        end_date_str: Optional[str] = None

        if query.year and query.week:
            start_dt, end_dt = date_get_range_from_year_and_week(query.year, query.week)
            start_date_str = start_dt
            end_date_str = end_dt
            self.logger.info(f"Fetching data by year={query.year}, week={query.week}")
        elif query.start_date and query.end_date:
            start_date_str = date_str_from_date_obj(query.start_date)
            end_date_str = date_str_from_date_obj(query.end_date)
            self.logger.info(f"Fetching data by start_date={query.start_date}, end_date={query.end_date}")
        elif query.start_date and not query.end_date:
            start_date_str = date_str_from_date_obj(query.start_date)
            self.logger.info(f"Fetching data by start_date={query.start_date}")
        else:
            self.logger.warning("No date parameters provided, returning empty list")
            return []


        # Fetch results
        _result: list[HourByHourModel] = []
        if end_date_str:
            await scoped_execute_async(
                session_factory=self.hbh_dao.session,
                query_function=lambda s: self.hbh_dao.fetch_get_all_record_by_date_range(start_date_str, end_date_str),
                on_complete=lambda q_res: _result.extend(translate_hour_by_hour_schema_list_to_model_list(q_res)),
                handle_http_error=http_handle_error
            )
        else:
            await scoped_execute_async(
                session_factory=self.hbh_dao.session,
                query_function=lambda s: self.hbh_dao.fetch_get_all_record_by_date(start_date_str),
                on_complete=lambda q_res: _result.extend(translate_hour_by_hour_schema_list_to_model_list(q_res)),
                handle_http_error=http_handle_error
            )

        self.logger.info(f"Returning {len(_result)} records")

        return _result
