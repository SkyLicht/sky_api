import json

from core.data.dao.hbh_dao import WorkPlanDAO
from core.data.handlers.handler_hour_by_hour import handle_weekly_kpi
from core.data.models.request_model import RequestWeekEffModel
from core.db.database import DBConnection
from core.db.util import scoped_execute, http_handle_error

if __name__ == '__main__':

    session =DBConnection().get_session()

