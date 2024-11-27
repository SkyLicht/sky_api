import asyncio

from core.data.dao.hbh_dao import HbhDAO
from core.db.database import DBConnection
from core.features.hour_by_hour.hbh_handlers import  pb_to_db, pb_to_json
from core.features.hour_by_hour.hbh_service import HbhService

if __name__ == "__main__":
    #pb_to_json(days=365, dir="config/data")

    dao = HbhDAO(DBConnection().get_session())
    service = HbhService(dao)

    asyncio.run(service.update_day_before())

    #asyncio.run(service.update_currently_hour())
