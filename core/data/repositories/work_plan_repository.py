from core.data.dao.hbh_dao import WorkPlanDAO
from core.data.models.hour_by_hour_model import WorkPlanModel
from core.db.util import scoped_execute, http_handle_error


class WorkPlanRepository:
    def __init__(self, db):
        self.dao = WorkPlanDAO(db)

    def create_work_plan(self, work_plan: WorkPlanModel):
        schema = work_plan.to_schema('A6')
        scoped_execute(
            session_factory=self.dao.session,
            query_function=lambda _session: self.dao.query_create_record(schema),
            on_complete=lambda query_result: print(f"Work Plan added successfully"),
            handle_error=http_handle_error
        )
        return work_plan