import argparse
from sqlite3 import IntegrityError

from core.db.database import DBConnection
from core.data.models.user_model import User, Role, Permission
from core.security.auth import get_password_hash




def init_db():
    session = DBConnection().get_session()
    try:
        # Fetch or create permissions
        def get_or_create_permission(name):
            permission = session.query(Permission).filter_by(name=name).first()
            if not permission:
                permission = Permission(name=name)
                session.add(permission)
                session.commit()
            return permission

        read_permission = get_or_create_permission("read")
        write_permission = get_or_create_permission("write")
        delete_permission = get_or_create_permission("delete")

        # Fetch or create the admin role
        admin_role = session.query(Role).filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(name="admin", permissions=[read_permission, write_permission, delete_permission])
            session.add(admin_role)
            session.commit()

        user_role = session.query(Role).filter_by(name="user").first()
        if not user_role:
            admin_role = Role(name="user", permissions=[read_permission, write_permission, delete_permission])
            session.add(admin_role)
            session.commit()

        # Fetch or create the user
        iradi_user = session.query(User).filter_by(username="iradi").first()
        if not iradi_user:
            iradi_user = User(username="iradi", hashed_password=get_password_hash('root'))  # Replace with a hashed password
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



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage database')
    parser.add_argument(
        '--db',
        type=str,
        choices=['init', 'aau'],
        help='...'
    )

    arg = parser.parse_args()

    if arg.db == 'init':
        init_db()



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