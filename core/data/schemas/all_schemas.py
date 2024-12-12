
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Index, CheckConstraint, Date, UniqueConstraint, \
    DateTime, func
from sqlalchemy.orm import relationship, backref

from core.db.database import Base
from core.db.util import generate_16_uuid

class EmployeeSchema(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        CheckConstraint("shift IN ('first', 'second', 'third')", name='valid_shift'),
    )

    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
    clock_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    shift = Column(String(16), nullable=False, default='first', server_default='first')
    image = Column(String(255), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)
    factory = Column(String(10), nullable=False)
    supervisor_id = Column(String(16), ForeignKey('employees.id'), nullable=True)
    department_id = Column(String(16), ForeignKey('departments.id'), nullable=False)
    position_id = Column(String(16), ForeignKey('positions.id'), nullable=False)

    # Relationships
    work_records = relationship('WorkRecordSchema', back_populates='employee', cascade="all, delete-orphan")
    supervisor = relationship(
        'EmployeeSchema',
        remote_side=[id],
        backref=backref('subordinates', cascade="all, delete-orphan")
    )
    department = relationship('DepartmentSchema', back_populates='employees')
    position = relationship('PositionSchema', back_populates='employees')

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Employee(name='{self.name}', position='{self.position}', department='{self.department}')>"



# Association table for sections and assignments
class DepartmentSchema(Base):
    __tablename__ = 'departments'

    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    factory = Column(String(10), nullable=False)

    employees = relationship('EmployeeSchema', back_populates='department')

    def __repr__(self):
        return f"<Department(name='{self.name}')>"


class PositionSchema(Base):
    __tablename__ = 'positions'

    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)

    employees = relationship('EmployeeSchema', back_populates='position')

    def __repr__(self):
        return f"<Position(name='{self.name}')>"
# Class representing lines
class LineSchema(Base):
    __tablename__ = 'lines'

    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    factory = Column(String(10), nullable=False)
    # Relationship with work records
    work_records = relationship('WorkRecordSchema', back_populates='line')

    # In LineSchema
    layout = relationship('LayoutSchema', back_populates='line', cascade="all, delete-orphan", lazy='select')

    def __repr__(self):
        return f"<Line(name='{self.name}')>"

    def to_dict(self)-> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "factory": self.factory
        }


# Class representing sections
class SectionSchema(Base):
    __tablename__ = 'sections'
    __table_args__ = (
        UniqueConstraint('nickname', 'factory', name='unique_name_factory'),
    )

    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
    name = Column(String, nullable=False)
    nickname = Column(String(10), nullable=False)
    factory = Column(String(10), nullable=False)

    # Relationship with work records
    work_records = relationship('WorkRecordSchema', back_populates='section')
    def __repr__(self):
        return f"<Section(name='{self.name}')>"

# Class representing assignments
class AssignmentSchema(Base):
    __tablename__ = 'assignments'

    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    # Relationship with work records
    work_records = relationship('WorkRecordSchema', back_populates='assignment')

    def __repr__(self):
        return f"<Assignment(description='{self.description}')>"

# Class representing employee work records
class WorkRecordSchema(Base):
    __tablename__ = 'work_records'
    __table_args__ = (
        CheckConstraint("shift IN ('first', 'second', 'third')", name='valid_shift'),
    )

    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
    shift = Column(String, nullable=False, default='first', server_default='first')
    date = Column(Date, nullable=False)
    week = Column(Integer, nullable=False)
    factory = Column(String(10), nullable=False)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)  # Description of the assignment
    line_id = Column(Integer, ForeignKey('lines.id'), nullable=False)
    employee_id = Column(String(16), ForeignKey('employees.id'), nullable=False)
    section_id = Column(String(16), ForeignKey('sections.id'), nullable=False)
    # Relationships
    section = relationship('SectionSchema', back_populates='work_records')
    employee = relationship('EmployeeSchema', back_populates='work_records')
    line = relationship('LineSchema', back_populates='work_records')
    assignment = relationship('AssignmentSchema', back_populates='work_records')

    def __repr__(self):
        return f"<WorkRecord(date='{self.date}', line='{self.line.name}', assignment='{self.assignment.description}')>"




class StationSchema(Base):
    __tablename__ = 'stations'
    __table_args__ = (
        UniqueConstraint('label', name='uq_station_name'),  # Enforce unique name
    )
    id = Column(String(16), primary_key=True, default=generate_16_uuid, unique=True, nullable=False)
    label = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)  # Made optional to allow flexibility
    is_automatic = Column(Boolean, nullable=False, default=True)

    # Relationships
    layout = relationship('LayoutSchema', back_populates='station', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Station(name='{self.name}')>"

class LayoutSectionSchema(Base):
    __tablename__ = 'layout_sections'
    __table_args__ = (
        UniqueConstraint('name', name='uq_layout_section_name'),  # Enforce unique name
    )

    id = Column(String(16), primary_key=True, default=generate_16_uuid, unique=True, nullable=False)
    index = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    area = Column(String(255), nullable=False)

    layout = relationship('LayoutSchema', back_populates='layout_section')



class MachineTypeSchema(Base):
    __tablename__ = 'machine_types'

    id = Column(String(16), primary_key=True, default=generate_16_uuid, unique=True, nullable=False)
    name = Column(String(255), nullable=False, unique=True)  # Enforce unique names for machine types
    description = Column(String(255), nullable=True)  # Made optional for flexibility
    machine_brand = Column(String(255), nullable=False)

    # Relationships
    machines = relationship('MachineSchema', back_populates='machine_type', cascade="all, delete-orphan")

class MachineSchema(Base):
    __tablename__ = 'machines'
    __table_args__ = (
        Index('idx_ip_serial_number', 'ip', 'serial_number', unique=True),
    )
    id = Column(String(16), primary_key=True, default=generate_16_uuid, unique=True, nullable=False)
    serial_number = Column(String(255), nullable=False, unique=True)  # Ensures each machine has a unique serial number
    ip = Column(String(255), nullable=False, unique=True)  # Ensures unique IP addresses for machines

    # Foreign Keys
    machine_type_id = Column(String(16), ForeignKey('machine_types.id'), nullable=False)

    # Relationships
    machine_type = relationship('MachineTypeSchema', back_populates='machines')

    # In LayoutSchema
    layout = relationship('LayoutSchema', back_populates='machine', cascade="all, delete-orphan", lazy='select')

class ClusterSchema(Base):
    __tablename__ = 'clusters'

    id = Column(String(16), primary_key=True, default=generate_16_uuid, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)  # Made optional for flexibility

    # Relationships
    layout = relationship('LayoutSchema', back_populates='cluster')




class LayoutSchema(Base):
    __tablename__ = 'layouts'

    id = Column(String(16), primary_key=True, default=generate_16_uuid, unique=True, nullable=False)
    index = Column(Integer, nullable=False)
    is_ct = Column(Boolean, nullable=False, default=False)
    version = Column(Integer, nullable=False)

    # Foreign Keys
    station_id = Column(String(16), ForeignKey('stations.id'), nullable=False)
    cluster_id = Column(String(16), ForeignKey('clusters.id'), nullable=True)
    line_id = Column(String(16), ForeignKey('lines.id'), nullable=False)
    machine_id = Column(String(16), ForeignKey('machines.id'), nullable=True)
    layout_section_id = Column(String(16), ForeignKey('layout_sections.id'), nullable=False)

    # Relationships
    station = relationship('StationSchema', back_populates='layout')
    cluster = relationship('ClusterSchema', back_populates='layout')
    line = relationship('LineSchema', back_populates='layout', lazy='select')
    machine = relationship('MachineSchema', back_populates='layout')
    layout_section = relationship('LayoutSectionSchema', back_populates='layout')

    def to_dict(self)-> dict:
        return {
            "id": self.id,
            "index": self.index,
            "is_ct": self.is_ct,
            "version": self.version,
            "station_id": self.station_id,
            "cluster_id": self.cluster_id,
            "line_id": self.line_id,
            "machine_id": self.machine_id,
            "layout_section_id": self.layout_section_id
        }

    def __repr__(self):
        return f"<Layout(index='{self.index}', version='{self.version}')> "