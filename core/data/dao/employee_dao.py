# DAO (Data Access Object) Classes
from core.data.schemas.employee_schema import EmployeeSchema, SectionSchema, AssignmentSchema, WorkRecordSchema, \
    LineSchema, DepartmentSchema, PositionSchema


class EmployeeDAO:
    @staticmethod
    def query_add_record(session, record: EmployeeSchema):
        session.add(record)
        session.commit()

    @staticmethod
    def query_add_records(session, records: list[EmployeeSchema]):
        for record in records:
            session.add(record)
        session.commit()

    @staticmethod
    def read(session, employee_id):
        return session.query(EmployeeSchema).filter_by(id=employee_id).first()

    @staticmethod
    def update(session, employee_id, **kwargs):
        employee = session.query(EmployeeSchema).filter_by(id=employee_id).first()
        for key, value in kwargs.items():
            setattr(employee, key, value)
        session.commit()
        return employee

    @staticmethod
    def delete(session, employee_id):
        employee = session.query(EmployeeSchema).filter_by(id=employee_id).first()
        session.delete(employee)
        session.commit()

class LineDAO:
    @staticmethod
    def query_add_record(session, record: LineSchema):
        session.add(record)
        session.commit()

    @staticmethod
    def query_add_records(session, records: list[LineSchema]):
        for record in records:
            session.add(record)
        session.commit()

    @staticmethod
    def read(session, line_id):
        return session.query(LineSchema).filter_by(id=line_id).first()

    @staticmethod
    def update(session, line_id, **kwargs):
        line = session.query(LineSchema).filter_by(id=line_id).first()
        for key, value in kwargs.items():
            setattr(line, key, value)
        session.commit()
        return line

    @staticmethod
    def delete(session, line_id):
        line = session.query(LineSchema).filter_by(id=line_id).first()
        session.delete(line)
        session.commit()

class SectionDAO:
    @staticmethod
    def query_add_record(session, record: SectionSchema):
        session.add(record)
        session.commit()

    @staticmethod
    def query_add_records(session, records: list[SectionSchema]):
        for record in records:
            session.add(record)
        session.commit()

    @staticmethod
    def read(session, section_id):
        return session.query(SectionSchema).filter_by(id=section_id).first()

    @staticmethod
    def update(session, section_id, **kwargs):
        section = session.query(SectionSchema).filter_by(id=section_id).first()
        for key, value in kwargs.items():
            setattr(section, key, value)
        session.commit()
        return section

    @staticmethod
    def delete(session, section_id):
        section = session.query(SectionSchema).filter_by(id=section_id).first()
        session.delete(section)
        session.commit()

class AssignmentDAO:
    @staticmethod
    def query_add_record(session, record: AssignmentSchema):
        session.add(record)
        session.commit()

    @staticmethod
    def query_add_records(session, records: list[AssignmentSchema]):
        for record in records:
            session.add(record)
        session.commit()



    @staticmethod
    def read(session, assignment_id):
        return session.query(AssignmentSchema).filter_by(id=assignment_id).first()

    @staticmethod
    def update(session, assignment_id, **kwargs):
        assignment = session.query(AssignmentSchema).filter_by(id=assignment_id).first()
        for key, value in kwargs.items():
            setattr(assignment, key, value)
        session.commit()
        return assignment

    @staticmethod
    def delete(session, assignment_id):
        assignment = session.query(AssignmentSchema).filter_by(id=assignment_id).first()
        session.delete(assignment)
        session.commit()

class WorkRecordDAO:
    @staticmethod
    def create(session, employee_id, shift, line_id, date, week, assignment_id):
        work_record = WorkRecordSchema(employee_id=employee_id, shift=shift, line_id=line_id, date=date, week=week, assignment_id=assignment_id)
        session.add(work_record)
        session.commit()
        return work_record

    @staticmethod
    def read(session, work_record_id):
        return session.query(WorkRecordSchema).filter_by(id=work_record_id).first()

    @staticmethod
    def update(session, work_record_id, **kwargs):
        work_record = session.query(WorkRecordSchema).filter_by(id=work_record_id).first()
        for key, value in kwargs.items():
            setattr(work_record, key, value)
        session.commit()
        return work_record

    @staticmethod
    def delete(session, work_record_id):
        work_record = session.query(WorkRecordSchema).filter_by(id=work_record_id).first()
        session.delete(work_record)
        session.commit()

class DepartmentDAO:
    @staticmethod
    def query_add_record(session, record: DepartmentSchema):
        session.add(record)
        session.commit()

    @staticmethod
    def query_add_records(session, records: list[DepartmentSchema]):
        for record in records:
            session.add(record)
        session.commit()

    @staticmethod
    def read(session, department_id):
        return session.query(DepartmentSchema).filter_by(id=department_id).first()

    @staticmethod
    def update(session, department_id, **kwargs):
        department = session.query(DepartmentSchema).filter_by(id=department_id).first()
        for key, value in kwargs.items():
            setattr(department, key, value)
        session.commit()
        return department

    @staticmethod
    def delete(session, department_id):
        department = session.query(DepartmentSchema).filter_by(id=department_id).first()
        session.delete(department)
        session.commit()

class PositionDAO:
    @staticmethod
    def query_add_record(session, record: PositionSchema):
        session.add(record)
        session.commit()

    @staticmethod
    def query_add_records(session, records: list[PositionSchema]):
        for record in records:
            session.add(record)
        session.commit()

    @staticmethod
    def read(session, position_id):
        return session.query(PositionSchema).filter_by(id=position_id).first()

    @staticmethod
    def update(session, position_id, **kwargs):
        position = session.query(PositionSchema).filter_by(id=position_id).first()
        for key, value in kwargs.items():
            setattr(position, key, value)
        session.commit()
        return position

    @staticmethod
    def delete(session, position_id):
        position = session.query(PositionSchema).filter_by(id=position_id).first()
        session.delete(position)
        session.commit()