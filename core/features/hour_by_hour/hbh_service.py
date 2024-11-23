import logging
from datetime import datetime
from core.features.hour_by_hour.hbh_mackenzie_api import api_respond_to_model, get_hour_by_hour
from core.features.util.date_util import transform_date_to_mackenzie

class HbhService:
    def __init__(self, dao):
        self.hbh_dto = dao

    async def update_at_intervals(self):
        try:
            get_current_day = datetime.now().strftime("%Y-%m-%d")
            get_current_hour_in_string = datetime.now().strftime("%H")
            responds = api_respond_to_model(
                get_hour_by_hour(transform_date_to_mackenzie(get_current_day), get_current_hour_in_string),
                get_current_day,
            )

            for keys, records in responds.items():
                for record in records:
                    self.hbh_dto.query_update_last_hour(record.to_schema())



        except Exception as e:
            logging.error(f"Error occurred during update: {e}")

    async def update_at_first_minute_of_the_hour(self):
        print("Updating at first minute of the hour")