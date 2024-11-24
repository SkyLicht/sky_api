from core.data.schemas.employee_schema import SectionSchema, AssignmentSchema, DepartmentSchema, PositionSchema
from core.data.types import SectionNickname

assignment_ing = AssignmentSchema(name="Engineer")
assignment_sup = AssignmentSchema(name="Supervisor")
assignment_tech = AssignmentSchema(name="Technician")
assignment_op = AssignmentSchema(name="Operator")


def return_assignments():
    return [assignment_ing, assignment_sup, assignment_tech, assignment_op]


departments_schemas = [
    DepartmentSchema(name="Automation", factory='A6'),
    DepartmentSchema(name="Equipment", factory='A6'),
    DepartmentSchema(name="Industrial Engineer", factory='A6'),
    DepartmentSchema(name="Production", factory='A6'),
    DepartmentSchema(name="Programing", factory='A6'),
    DepartmentSchema(name="Quality", factory='A6'), ]


def return_sections():
    return departments_schemas

positions_schemas = [
    PositionSchema(name="Engineer"),
    PositionSchema(name="Supervisor"),
    PositionSchema(name="Technician SMT"),
]

def return_positions():
    return positions_schemas

sections_schemas = [
    SectionSchema(name="Automation", nickname=SectionNickname.AU.value, factory='A6'),
    SectionSchema(name="Equipment SMT", nickname=SectionNickname.EES.value, factory='A6'),
    SectionSchema(name="Equipment Packing", nickname=SectionNickname.EEP.value, factory='A6'),
    SectionSchema(name="Production", nickname=SectionNickname.PD.value, factory='A6'),
    SectionSchema(name="Industrial Engineering", nickname=SectionNickname.IE.value, factory='A6'),
    SectionSchema(name="Quality", nickname=SectionNickname.QA.value, factory='A6'), ]
