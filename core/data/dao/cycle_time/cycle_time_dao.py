from sqlalchemy.orm import joinedload

from core.data.models.cycle_time_model import CycleTimeModel
from core.data.schemas.all_schemas import CycleTimeRecordSchema, CycleTimeSchema, LayoutSchema


class CycleTimeDAO:

    def __init__(self, session):
        self.session = session

    async def fetch_create_record(self, record: CycleTimeRecordSchema) -> 'CycleTimeRecordSchema':
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    async def fetch_get_by_week(self, week):
        return self.session.query(CycleTimeRecordSchema).options(
            joinedload(CycleTimeRecordSchema.line),
            joinedload(CycleTimeRecordSchema.platform),
            joinedload(CycleTimeRecordSchema.user),
        ).filter_by(week=week).all()

    async def fetch_delete_record(self, record_id):
        self.session.query(CycleTimeRecordSchema).filter_by(id=record_id).delete()
        self.session.commit()
        return True

    async def fetch_get_by_id(self, record_id):
        return self.session.query(CycleTimeRecordSchema).options(
            joinedload(CycleTimeRecordSchema.cycle_times).joinedload(CycleTimeSchema.layout),
            joinedload(CycleTimeRecordSchema.cycle_times).joinedload(CycleTimeSchema.layout).joinedload(
                LayoutSchema.station),
            joinedload(CycleTimeRecordSchema.line),
            joinedload(CycleTimeRecordSchema.platform),
            joinedload(CycleTimeRecordSchema.user)).filter_by(id=record_id).first()

    async def fetch_update_cycle_time(self, cycle_time_id: str, cycles):

        self.session.query(CycleTimeSchema).filter(CycleTimeSchema.id == cycle_time_id).update({"cycles": cycles})
        self.session.commit()

        # Fetch the updated record
        #updated_record = self.session.query(CycleTimeSchema).filter_by(id=cycle_time_id).first()