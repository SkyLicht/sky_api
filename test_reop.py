import json

from core.data.dao.hbh_dao import WorkPlanDAO
from core.data.handlers.handler_hour_by_hour import handle_weekly_kpi
from core.data.models.request_model import RequestWeekEffModel
from core.db.database import DBConnection
from core.db.util import scoped_execute, http_handle_error

if __name__ == '__main__':
    session = DBConnection().get_session()
    dao = WorkPlanDAO(session)

    data = {
        "year": 2024,
        "week": 47,
        "dates": [
            {
                "day": "2024-11-21",
                "lines": [
                    {
                        "name": "J09",
                        "output": "output",
                        "shift": "first"
                    }, {
                        "name": "J01",
                        "output": "output",
                        "shift": "first"
                    }
                ]
            },
            {
                "day": "2024-11-22",
                "lines": [
                    {
                        "name": "J09",
                        "output": "packing",
                        "shift": "first"
                    }, {
                        "name": "J01",
                        "output": "packing",
                        "shift": "first"
                    }
                ]
            }
        ]
    }

    request_body = RequestWeekEffModel(**data)
    db_result = scoped_execute(
        session_factory=session,
        query_function=lambda _session: dao.get_work_hour_by_week(week=data.get('week')),
        on_complete=lambda query_result: print(f'data fetched'),
        handle_error=http_handle_error
    )

    if db_result.data is None:
        print("No data")

    _data = db_result.data

    ie_kpi = handle_weekly_kpi(request_body, _data)
    print(json.dumps(ie_kpi, indent=4))
