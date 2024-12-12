import json
from datetime import datetime

from aiohttp.helpers import set_exception

from core.data.dao.hbh_dao import WorkPlanDAO
from core.data.handlers.handler_hour_by_hour import handle_weekly_kpi
from core.data.models.cycle_time_model import CycleTimeInputModel, CycleTimeModel
from core.data.models.request_model import RequestWeekEffModel
from core.data.schemas.cycle_time_schema import CycleTimeSchema
from core.db.database import DBConnection
from core.db.util import scoped_execute, http_handle_error

if __name__ == '__main__':

    session =DBConnection().get_session()
    json_data = {
        "str_date": "2021-01-01",
        "week": 1,
        "cycles": [
            {
                "type": "na",
                "start": 1.0,
                "end": 1.0,
                "time": 1.0,
                "created": datetime.now().isoformat()
            }
        ],
        "platform_id": "cujtjjhpgyb2lg0",
        "line_id": "lxL6Pz3KSOmnefj"
    }





    try:
        schema = CycleTimeSchema.create_cycle_time_schema(
            str_date=json_data['str_date'],
            week=json_data['week'],
            cycles=json_data['cycles'],
            line_id=json_data['line_id'],
            platform_id=json_data['platform_id']
        )
        session.add(schema)
        session.commit()  # Commit to persist the data
        session.refresh(schema)  # Refresh the instance to reflect the database state
        #print(schema.to_json())  # Print the schema
        print(
            CycleTimeInputModel.from_schema(schema).model_dump_json(indent=4)
        )
        session.close()  # Close the session
        #return schema  # Return the schema


    except Exception as e:
        print(e)
        # session.rollback()

    # tt= CycleTimeInputModel(
    #     id='1',
    #     line='1',
    #     platform='1',
    #     cycles=[CycleTimeModel(
    #         type= "na",
    #         start= 1.0,
    #         end= 1.0,
    #         time=1.0,
    #         created= datetime.now().isoformat()
    #     )]
    # )
    #
    # print(tt.to_json())
    #



