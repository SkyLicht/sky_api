import logging
from datetime import datetime, timedelta

from core.data.schemas.hour_by_hour_schema import HourByHourSchema
from core.features.hour_by_hour.hbh_mackenzie_api import api_respond_to_model, get_hour_by_hour, get_all_day
from core.features.util.date_util import transform_date_to_mackenzie, transform_range_of_dates


class HbhService:
    def __init__(self, dao):
        self.hbh_dto = dao

    async def update_currently_hour(self):
        try:
            get_current_day = datetime.now().strftime("%Y-%m-%d")
            get_current_hour_in_string = datetime.now().strftime("%H")
            responds = await api_respond_to_model(
                get_hour_by_hour(transform_date_to_mackenzie(get_current_day), get_current_hour_in_string),
                get_current_day,
            )

            if responds is None:
                logging.error("No response from the API")
                return

            self.hbh_dto.query_update_hours([record.to_schema("A6") for record in responds.values()])

        except Exception as e:
            logging.error(f"Error occurred during update: {e}")

    async def update_day_hours(self):
        try:
            get_current_day = datetime.now().strftime("%Y-%m-%d")
            responds = await api_respond_to_model(
                get_all_day(transform_date_to_mackenzie(get_current_day)),
                get_current_day,
            )

            self.hbh_dto.query_update_hours([record.to_schema("A6") for record in responds.values()])

        except Exception as e:
            logging.error(f"Error occurred during update: {e}")



    async def update_previews_day(self):

        try:
            get_current_day = datetime.now().strftime("%Y-%m-%d")
            responds =  await api_respond_to_model(
                get_all_day(transform_date_to_mackenzie(get_current_day)),
                get_current_day,
            )

            if responds is None:
                logging.error("No response from the API")
                return

            self.hbh_dto.query_update_hours([record.to_schema("A6") for record in responds.values()])

            return True

        except Exception as e:
            logging.error(f"Error occurred during update: {e}")

    async def update_hours_form_range_of_dates(self, start_date: str, end_date: str):
        try:
            _responds: list[HourByHourSchema] = []
            dates = transform_range_of_dates(form=start_date, at=end_date)
            for date in dates:
                responds = await api_respond_to_model(
                    data=get_all_day(day=transform_date_to_mackenzie(date)),
                    date=date
                )
                _responds.extend([record.to_schema("A6") for record in responds.values()])

            self.hbh_dto.query_update_hours(_responds)

        except Exception as e:
            logging.error(f"Error occurred during update: {e}")

    async def update_hours_at_day(self, date: str):
        try:
            responds = await api_respond_to_model(
                data=get_all_day(day=transform_date_to_mackenzie(date)),
                date=date
            )
            self.hbh_dto.query_update_hours([record.to_schema("A6") for record in responds.values()])

        except Exception as e:
            logging.error(f"Error occurred during update: {e}")




import asyncio

if __name__ == "__main__":
    # dao = HbhDAO(DBConnection().get_session())
    # service = HbhService(dao)
    #
    # asyncio.run(service.update_hours_form_range_of_dates("2021-09-01", "2021-09-25"))

    #asyncio.run(service.update_hours_of_day_before())
    pass

