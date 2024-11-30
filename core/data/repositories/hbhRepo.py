import json

from requests import session

from core.data.dao.hbh_dao import WorkPlanDAO, HbhDAO
from core.data.handlers.handler_hour_by_hour import handle_weekly_kpi
from core.data.models.request_model import RequestWeekEffModel
from core.db.util import scoped_execute, http_handle_error
from core.features.hour_by_hour.hbh_service import HbhService


class HourByHourRepository:

    def __init__(self, db):
        self.dao = WorkPlanDAO(db)
        self.hbh_dao = HbhDAO(db)

    async def get_eff_by_week(self, data: dict):

        result = scoped_execute(
            session_factory=self.dao.session,
            query_function=lambda _session: self.dao.get_work_hour_by_week(week=data.get('week')),
            on_complete=lambda query_result: print(f'data fetched'),
            handle_error=http_handle_error
        )

        _result = []

        if result.data:
            for record in data.get('dates'):
                _record = result.data.get(record['date'])
                _temp = []
                if _record:
                    for line in record['lines']:
                        if line in _record:
                            third_shift_smt = [output['smt_out'] for output in
                                               _record.get(line).get('hour_by_hour')[0:6]]
                            third_shift_packing = [output['packing'] for output in
                                                   _record.get(line).get('hour_by_hour')[0:6]]

                            first_shift_smt = [output['smt_out'] for output in
                                               _record.get(line).get('hour_by_hour')[6:16]]
                            first_shift_packing = [output['packing'] for output in
                                                   _record.get(line).get('hour_by_hour')[6:16]]

                            second_shift_smt = [output['packing'] for output in
                                                _record.get(line).get('hour_by_hour')[16:23]]
                            second_shift_packing = [output['packing'] for output in
                                                    _record.get(line).get('hour_by_hour')[16:23]]

                            uph_i = (_record.get(line).get('platform').get('uph') * _record.get(line).get(
                                'work_plan').get('target_oee'))

                            third_commit = round(uph_i * 6.25)
                            first_commit = round(uph_i * 9.25)
                            second_commit = round(uph_i * 7.75)

                            _temp.append({
                                "line": line,
                                "date": record['date'],
                                "uph": round(uph_i),
                                # "target_oee": _record.get(line).get('work_plan').get('target_oee'),
                                "third_shift": {
                                    "commit": third_commit,
                                    "smt": sum(third_shift_smt),
                                    "packing": sum(third_shift_packing),
                                    "eff_smt": round((sum(third_shift_smt) / third_commit) * 100, 2),
                                    "eff_packing": round((sum(third_shift_packing) / third_commit) * 100, 2)
                                },
                                "first_shift": {
                                    "commit": first_commit,
                                    "smt": sum(first_shift_smt),
                                    "packing": sum(first_shift_packing),
                                    "eff_smt": round((sum(first_shift_smt) / first_commit) * 100, 2),
                                    "eff_packing": round((sum(first_shift_packing) / first_commit) * 100, 2)
                                },
                                "second_shift": {
                                    "commit": second_commit,
                                    "smt": sum(second_shift_smt),
                                    "packing": sum(second_shift_packing),
                                    "eff_smt": round((sum(second_shift_packing) / second_commit) * 100, 2),
                                    "eff_packing": round((sum(second_shift_packing) / second_commit) * 100, 2)

                                }
                            })

                _result.append({
                    "date": record['date'],
                    # "lines": _temp,
                    "gen_eff": {
                        "third_shift": {
                            "smt": [{"line": record['line'], "eff": record['third_shift']['eff_smt']} for record in
                                    _temp],
                            "packing": [{"line": record['line'], "eff": record['third_shift']['eff_packing']} for record
                                        in
                                        _temp]
                        },
                        "first_shift": {
                            "smt": [{"line": record['line'], "eff": record['first_shift']['eff_smt']} for record in
                                    _temp],
                            "packing": [{"line": record['line'], "eff": record['first_shift']['eff_packing']} for record
                                        in
                                        _temp]
                        },
                        "second_shift": {
                            "smt": [{"line": record['line'], "eff": record['second_shift']['eff_smt']} for record in
                                    _temp],
                            "packing": [{"line": record['line'], "eff": record['second_shift']['eff_packing']} for
                                        record in
                                        _temp]
                        }
                    }
                })
                # print(json.dumps(_result, indent=4))

            return _result
        return []

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
        service = HbhService(dao=self.hbh_dao)
        return service.update_previews_day()

    async def update_range_of_dates(self, start_date: str, end_date: str):
        service = HbhService(dao=self.hbh_dao)
        _responds = await service.update_hours_form_range_of_dates(start_date, end_date)
        return _responds
