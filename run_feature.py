import argparse
import asyncio
from datetime import datetime

from core.data.dao.hbh_dao import HbhDAO
from core.db.database import DBConnection
from core.features.hour_by_hour.hbh_service import  HbhService
from core.features.task_handler import AsyncPeriodicExecutor, logger

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run')
    parser.add_argument(
        '--feature_name',
        type=str,
        choices=['async_ex'],
        help='...'
    )
    arg = parser.parse_args()
    if arg.feature_name == 'async_ex':
        # Path to the JSON file containing task definitions
        json_file_path = 'config/tasks.json'

        # Create an instance of the executor
        executor = AsyncPeriodicExecutor("api_db")

        # Schedule the tasks

        async def ttes():
            print("Hello")

        hbh_service = HbhService(dao=HbhDAO(connection=DBConnection().get_session()))

        async def schedule_tasks():

            await executor.schedule_task(hbh_service.update_currently_hour, interval_seconds=30)
            await executor.schedule_task(hbh_service.update_day_hours, hourly=True)
            await executor.schedule_task(hbh_service.update_previews_day, daily= "01:00")


        async def main():
            await schedule_tasks()
            try:
                await executor.start()
            except KeyboardInterrupt:
                logger.info("KeyboardInterrupt received. Stopping the executor...")
                # Signal the executor to stop
                executor.stop_event.set()
                # Wait for the executor to finish cleaning up
                await executor.loop_task


        asyncio.run(main())
