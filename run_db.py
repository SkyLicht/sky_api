import argparse
from sqlite3 import IntegrityError

from requests import session

from core.data.dao.employee_dao import LineDAO, SectionDAO, AssignmentDAO, EmployeeDAO, PositionDAO, DepartmentDAO
from core.data.schemas.defaults_schema import sections_schemas, return_assignments, positions_schemas, \
    departments_schemas
from core.data.schemas.employee_schema import LineSchema, EmployeeSchema, SectionSchema, AssignmentSchema, \
    WorkRecordSchema
from core.data.schemas.hour_by_hour_schema import HourByHourSchema, WorkPlanSchema, PlatformSchema
from core.data.schemas.user_schema import UserSchema, RoleSchema, RouteSchema, PermissionSchema
from core.data.types import SectionNickname
from core.db.database import DBConnection

from core.db.util import safe_execute
from core.security.auth import get_password_hash

from core.data.schemas.hour_by_hour_schema import HourByHourSchema, WorkPlanSchema, PlatformSchema


def create_tables():
    # Create tables
    DBConnection().create_table(EmployeeSchema)
    DBConnection().create_table(LineSchema)
    DBConnection().create_table(SectionSchema)
    DBConnection().create_table(AssignmentSchema)
    DBConnection().create_table(WorkRecordSchema)
    DBConnection().create_table(HourByHourSchema)
    DBConnection().create_table(WorkPlanSchema)
    DBConnection().create_table(PlatformSchema)
    DBConnection().create_table(UserSchema)
    DBConnection().create_table(RoleSchema)
    DBConnection().create_table(RouteSchema)
    DBConnection().create_table(PermissionSchema)
    print('Database initialized')


def populate_user():


    session = DBConnection().get_session()
    try:
        # Fetch or create permissions
        def get_or_create_permission(name):
            permission = session.query(PermissionSchema).filter_by(name=name).first()
            if not permission:
                permission = PermissionSchema(name=name)
                session.add(permission)
                session.commit()
            return permission

        read_permission = get_or_create_permission("read")
        write_permission = get_or_create_permission("write")
        delete_permission = get_or_create_permission("delete")

        # Fetch or create the admin role
        admin_role = session.query(RoleSchema).filter_by(name="admin").first()
        if not admin_role:
            admin_role = RoleSchema(name="admin", permissions=[read_permission, write_permission, delete_permission])
            session.add(admin_role)
            session.commit()

        user_role = session.query(RoleSchema).filter_by(name="user").first()
        if not user_role:
            user_role = RoleSchema(name="user", permissions=[read_permission, write_permission, delete_permission])
            session.add(user_role)
            session.commit()

        # Fetch or create the user
        iradi_user = session.query(UserSchema).filter_by(username="iradi").first()
        if not iradi_user:
            iradi_user = UserSchema(username="iradi",
                              hashed_password=get_password_hash('root'))  # Replace with a hashed password
            session.add(iradi_user)
            session.commit()

        # Associate the role with the user
        if admin_role not in iradi_user.roles:
            iradi_user.roles.append(admin_role)
            session.commit()
            print("Role 'admin' added to user 'iradi'.")
        else:
            print("User 'iradi' already has the 'admin' role.")


    except IntegrityError as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()



def populate_employee():
    #Composite lambda to execute all queries in one transaction
    # Callbacks
    # on_complete = lambda result: print("All queries executed successfully.")
    # on_error = lambda e: print(f"An error occurred: {e}")
    # on_finally = lambda: print("Query execution finished.")


    safe_execute(
        session_factory=DBConnection().get_session,
        query_function=lambda _session: (
            LineDAO().query_add_records(
                _session,
                [
                    LineSchema(name='J01', factory='A6'),
                    LineSchema(name='J02', factory='A6'),
                    LineSchema(name='J03', factory='A6'),
                    LineSchema(name='J05', factory='A6'),
                    LineSchema(name='J06', factory='A6'),
                    LineSchema(name='J07', factory='A6'),
                    LineSchema(name='J08', factory='A6'),
                    LineSchema(name='J09', factory='A6'),
                ]
            ),
            SectionDAO.query_add_records(_session, sections_schemas),
            AssignmentDAO.query_add_records(_session, return_assignments()),
            PositionDAO.query_add_records(_session, positions_schemas),
            DepartmentDAO.query_add_records(_session, departments_schemas),
            EmployeeDAO.query_add_record(_session, EmployeeSchema(
                clock_id='123456',
                name='Iradi',
                last_name='Mendoza',
                shift='first',
                factory='A6',
                department_id=departments_schemas[2].id,
                position_id=positions_schemas[0].id,
                is_active=True
            )),
        )
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage database')
    parser.add_argument(
        '--db',
        type=str,
        choices=['pop_user', 'create_tables', 'pop_employee'],
        help='...'
    )

    arg = parser.parse_args()

    if arg.db == 'pop_user':
        populate_user()
    elif arg.db == 'pop_employee':
        populate_employee()
    elif arg.db == 'create_tables':
        create_tables()

# def add_route_to_user(db: Session, route_path: str, username: str, description: str = None):
#     # Fetch or create the route
#     route = db.query(Route).filter_by(path=route_path).first()
#     if not route:
#         route = Route(path=route_path, description=description)
#         db.add(route)
#         db.commit()
#
#     # Fetch the user
#     user = db.query(User).filter_by(username=username).first()
#     if not user:
#         raise ValueError(f"User '{username}' does not exist.")
#
#     # Associate the route with the user
#     if route not in user.routes:
#         user.routes.append(route)
#         db.commit()
#         print(f"Route '{route_path}' added to user '{username}'.")
#     else:
#         print(f"Route '{route_path}' already associated with user '{username}'.")
