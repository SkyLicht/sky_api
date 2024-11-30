from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Text
from sqlalchemy.orm import relationship

from core.db.database import Base
from core.db.util import generate_16_uuid

user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('role_id', ForeignKey('roles.id'), primary_key=True)
)
# Association table for users and routes
user_routes = Table(
    'user_routes', Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('route_id', ForeignKey('routes.id'), primary_key=True)
)

role_permissions = Table(
    'role_permissions', Base.metadata,
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', ForeignKey('permissions.id'), primary_key=True)
)


class UserSchema(Base):
    __tablename__ = 'users'

    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    roles = relationship("RoleSchema", secondary=user_roles, back_populates="users")
    routes = relationship("RouteSchema", secondary=user_routes, back_populates="users")


class RouteSchema(Base):
    __tablename__ = 'routes'

    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
    path = Column(String, unique=True, index=True)  # Route path
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)  # Optional description of the route

    # Relationships
    users = relationship("UserSchema", secondary=user_routes, back_populates="routes")

class RoleSchema(Base):
    __tablename__ = 'roles'

    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
    name = Column(String, unique=True)

    users = relationship("UserSchema", secondary=user_roles, back_populates="roles")
    permissions = relationship("PermissionSchema", secondary=role_permissions, back_populates="roles")


class PermissionSchema(Base):
    __tablename__ = 'permissions'

    id = Column(String(16), primary_key=True, default=lambda: str(generate_16_uuid()), unique=True, nullable=False)
    name = Column(String, unique=True)

    roles = relationship("RoleSchema", secondary=role_permissions, back_populates="permissions")


