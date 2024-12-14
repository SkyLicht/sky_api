import json

from fastapi import HTTPException

from core.data.dao.cycle_time.cycle_time_dao import CycleTimeDAO
from core.data.dao.cycle_time.layout_dao import LayoutDAO
from core.data.models.cycle_time_model import CycleTimeModel
from core.data.models.layout_model import LayoutModel
from core.data.schemas.all_schemas import CycleTimeRecordSchema


class CycleTimeRepository:

    def __init__(self, db):
        self.db = db
        self.ct_dao = CycleTimeDAO(db)
        self.layout_dao = LayoutDAO(db)

    async def create_record(self, request) -> CycleTimeRecordSchema | None:

        try:
            # Fetch layout by line ID
            layouts = await self.layout_dao.fetch_get_layout_by_line_id(request.line)

            if not layouts:
                raise HTTPException(status_code=404, detail="No layout found for the specified line.")

            cycles_time: list[CycleTimeModel] = []

            # Initialize the CycleTimeRecordSchema
            ct_record_schema = CycleTimeRecordSchema(
                str_date=request.str_date,
                week=request.week,
                line_id=request.line,
                platform_id=request.platform,
            )

            # Generate cycle times from layouts
            ct_record_schema.cycle_times = [
                LayoutModel.from_schema(layout).to_cycle_time_schema(cycles_time) for layout in layouts
            ]
            # Create the record in the database
            record = await self.ct_dao.fetch_create_record(ct_record_schema)

            if not record:
                raise HTTPException(status_code=500, detail="Failed to create record.")

            return record


        except Exception as e:

            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            self.db.remove()

    async def get_by_week(self, week):

        try:
            records = await self.ct_dao.fetch_get_by_week(week)

            if not records:
                return []

            return records
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            self.db.remove()

    async def delete_record(self, record_id):

        try:
            record = await self.ct_dao.fetch_delete_record(record_id)

            if not record:
                raise HTTPException(status_code=404, detail="No record found for the specified ID.")

            return record
        except Exception as e:

            raise HTTPException(status_code=400, detail=str(e))
        finally:
            self.db.remove()

    async def get_by_id(self, record_id: str):
        try:
            record = await self.ct_dao.fetch_get_by_id(record_id)

            if not record:
                return {"data": None}

            return {"data": record}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            self.db.remove()

    async def update_cycle_time(self, cycle_time_id, cycles):
        try:
            await self.ct_dao.fetch_update_cycle_time(cycle_time_id, cycles)

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            self.db.remove()
