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

    async def get_by_week_details(self, week):
        try:
            records = await self.ct_dao.fetch_get_by_week(week)

            if not records:
                return []

            cts = []

            for record in records:
                # Construcción de la lista de cycle_times
                cycle_times_data = []
                for ct_record in record.cycle_times:
                    cycles = ct_record.cycles
                    valid_times = [c['time'] for c in cycles if c.get('time')]
                    average_time = sum(valid_times) / len(valid_times) if valid_times else 0

                    cycle_times_data.append({
                        "id": ct_record.id,
                        "average": average_time,
                        "index": ct_record.layout.index,
                        "station": ct_record.layout.station.label,
                        "section_area": ct_record.layout.layout_section.area,
                        "section_name": ct_record.layout.layout_section.name,
                        "cycles": cycles
                    })

                # Ordenar cycle_times por índice
                cycle_times_data = sorted(cycle_times_data, key=lambda x: x["index"])

                # Cálculo del número de cycle_times completados (aquellos con ciclos)
                cycle_times_completed = sum(1 for ct_time in cycle_times_data if len(ct_time["cycles"]) > 0)

                # Determinar el bottleneck (mayor promedio)
                bottleneck = max(cycle_times_data, key=lambda x: x["average"]) if cycle_times_data else {
                    "station": "",
                    "section_area": "",
                    "section_name": "",
                    "index": 0,
                    "average": 0,
                    "cycles": []
                }

                # Construcción del dict principal
                ct = {
                    "id": record.id,
                    "week": record.week,
                    "platform": record.platform.name,
                    "sku": record.platform.sku,
                    "uph": record.platform.uph,
                    "f_n": record.platform.f_n,
                    "line": record.line.name,
                    "factory": record.line.factory,
                    "created_at": record.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": record.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "cycle_times_length": len(cycle_times_data),
                    "cycle_times_completed": cycle_times_completed,
                    "bottle_neck": bottleneck,
                    "cycle_times": cycle_times_data
                }

                cts.append(ct)

            return cts

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
