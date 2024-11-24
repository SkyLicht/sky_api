from core.data.dao.user_dao import UserDAO
from core.data.models.user_model import CreateUserModel
from core.db.util import scoped_execute,http_handle_error


class UserRepository:
    def __init__(self, db):
        self.user_dao = UserDAO(db)

    def create_user(self, user: CreateUserModel):


        scoped_execute(
            session_factory=self.user_dao.session,
            query_function=lambda _session: self.user_dao.query_create_user(user),
            on_complete=lambda query_result: print(f"User  added successfully"),
            handle_error=http_handle_error
        )

        return user
