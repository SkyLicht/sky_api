from typing import Optional

from colorama import Fore, Style

from core.data.models.user_model import CreateUserModel
from core.data.schemas.user_schema import UserSchema, RoleSchema
from core.db.util import QueryResult, QueryResultError, QueryResultErrorType
from core.security.auth import get_password_hash


class UserDAO:

    def __init__(self, session):
        self.session = session

    def query_add_record(self, record: UserSchema) -> UserSchema:
        self.session.add(record)
        self.session.commit()
        return record

    def query_create_user(self, user: CreateUserModel) -> QueryResult:
        role = self.session.query(RoleSchema).filter_by(name=user.role).first()
        if not role:
            return QueryResult(data=None,
                               error=QueryResultError(message=f"Role: {user.role}. not found",
                                                      error_type=QueryResultErrorType.NOT_FOUND))
        user_schema = UserSchema(username=user.username, hashed_password=get_password_hash(user.password))
        user_schema.roles.append(role)
        _result = self.query_add_record(user_schema)
        return QueryResult(data=_result)
