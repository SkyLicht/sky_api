from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, UniqueConstraint, Table
from sqlalchemy.orm import relationship

from sqlalchemy.schema import CheckConstraint
from core.db.database import Base
from core.db.util import generate_16_uuid





# Class representing employees
# class EmployeeSchema(Base):
#     __tablename__ = 'employees'
#     __table_args__ = (
#         CheckConstraint("shift IN ('first', 'second', 'third')", name='valid_shift'),
#     )
#
#     id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
#     clock_id = Column(String, unique=True, nullable=False)  # Clock identifier
#     name = Column(String, nullable=False)
#     last_name = Column(String, nullable=False)
#     shift = Column(String, nullable=False, default='first', server_default='first')
#     image = Column(String, nullable=True)  # URL or path to the employee's image
#
#     is_active = Column(Boolean, nullable=False, default=True)
#     factory = Column(String(10), nullable=False)
#     supervisor_id = Column(Integer, ForeignKey('employees.id'), nullable=True)
#     department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
#     position_id = Column(Integer, ForeignKey('positions.id'), nullable=False)
#
#
#     # Relationship with work records
#     work_records = relationship('WorkRecordSchema', back_populates='employee')
#     supervisor = relationship('EmployeeSchema', remote_side=[id], backref='subordinates')
#     department = relationship('DepartmentSchema', backref='employees')
#     position = relationship('PositionSchema', backref='employees')
#
#
#     def __repr__(self):
#         return f"<Employee(name='{self.name}', position='{self.position}', department='{self.department}')>"
#
#
# # Association table for sections and assignments
# class DepartmentSchema(Base):
#     __tablename__ = 'departments'
#
#     id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
#     name = Column(String, unique=True, nullable=False)
#     factory = Column(String(10), nullable=False)
#
#     def __repr__(self):
#         return f"<Department(name='{self.name}')>"
#
#
# class PositionSchema(Base):
#     __tablename__ = 'positions'
#
#     id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
#     name = Column(String, unique=True, nullable=False)
#
#     def __repr__(self):
#         return f"<Position(name='{self.name}')>"
# # Class representing lines
# class LineSchema(Base):
#     __tablename__ = 'lines'
#
#     id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
#     name = Column(String, unique=True, nullable=False)
#     is_active = Column(Boolean, nullable=False, default=True)
#     factory = Column(String(10), nullable=False)
#     # Relationship with work records
#     work_records = relationship('WorkRecordSchema', back_populates='line')
#
#     # In LineSchema
#     layouts = relationship('LayoutSchema', back_populates='line', cascade="all, delete-orphan", lazy='select')
#
#     def __repr__(self):
#         return f"<Line(name='{self.name}')>"
#
# # Class representing sections
# class SectionSchema(Base):
#     __tablename__ = 'sections'
#     __table_args__ = (
#         UniqueConstraint('name', 'factory', name='unique_name_factory'),
#     )
#
#     id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
#     name = Column(String, nullable=False)
#     nickname = Column(String(10), nullable=False)
#     factory = Column(String(10), nullable=False)
#
#     # Relationship with work records
#     work_records = relationship('WorkRecordSchema', back_populates='section')
#     def __repr__(self):
#         return f"<Section(name='{self.name}')>"
#
# # Class representing assignments
# class AssignmentSchema(Base):
#     __tablename__ = 'assignments'
#
#     id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
#     name = Column(String, unique=True, nullable=False)
#     description = Column(String, nullable=True)
#
#     # Relationship with work records
#     work_records = relationship('WorkRecordSchema', back_populates='assignment')
#
#     def __repr__(self):
#         return f"<Assignment(description='{self.description}')>"
#
# # Class representing employee work records
# class WorkRecordSchema(Base):
#     __tablename__ = 'work_records'
#     __table_args__ = (
#         CheckConstraint("shift IN ('first', 'second', 'third')", name='valid_shift'),
#     )
#
#     id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
#     shift = Column(String, nullable=False, default='first', server_default='first')
#     date = Column(Date, nullable=False)
#     week = Column(Integer, nullable=False)
#     factory = Column(String(10), nullable=False)
#     assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)  # Description of the assignment
#     line_id = Column(Integer, ForeignKey('lines.id'), nullable=False)
#     employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
#     section_id = Column(Integer, ForeignKey('sections.id'), nullable=False)
#     # Relationships
#     section = relationship('SectionSchema', back_populates='work_records')
#     employee = relationship('EmployeeSchema', back_populates='work_records')
#     line = relationship('LineSchema', back_populates='work_records')
#     assignment = relationship('AssignmentSchema', back_populates='work_records')
#
#     def __repr__(self):
#         return f"<WorkRecord(date='{self.date}', line='{self.line.name}', assignment='{self.assignment.description}')>"
