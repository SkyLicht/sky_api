import random
import string
import uuid
import base64
from enum import Enum

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError


def generate_16_uuid():
    # Generate a UUID and remove the hyphens
    uuid_str = uuid.uuid4()

    # Convert UUID to bytes and then encode in Base64
    base64_uuid = base64.urlsafe_b64encode(uuid_str.bytes).decode("utf-8")

    # Remove specific unwanted characters
    clean_uuid = base64_uuid.translate(str.maketrans('', '', '/,-+*'))

    # Truncate the string to 16 characters
    short_uuid = clean_uuid[:16]

    return short_uuid


def generate_custom_id(length=15):
    # Define the characters for the custom ID
    characters = string.ascii_letters + string.digits

    # Randomly select `length` characters from the character set
    custom_id = ''.join(random.choices(characters, k=length))

    return custom_id

class QueryResultErrorType(Enum):
    """
    Enum to represent the type of error that occurred during a query.
    """
    NOT_FOUND = "NOT_FOUND"
    INVALID_REQUEST = "INVALID_REQUEST"
    DATABASE_ERROR = "DATABASE_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"

class QueryResultError:
    def __init__(self, message, error_type, tip=None):
        self.message = message
        self.error_type = error_type
        self.tip = tip

    def __str__(self):
        return f"QueryResultError(message={self.message}, error_type={self.error_type}, tip={self.tip})"


class QueryResult:
    def __init__(self,data=None, error= QueryResultError | None):
        self.data = data
        self.error = error

    def is_error(self):
        return self.error is not None

    def is_success(self):
        return self.error is None

    def __str__(self):
        return f"QueryResult(data={self.data}, error={self.error})"




def safe_execute(session_factory, query_function, *args, on_complete=None, on_error=None, on_finally=None, **kwargs):
    """
    Safely execute a database query with lifecycle callbacks for success, error, and cleanup.

    Args:
        session_factory (callable): A factory that provides a SQLAlchemy session.
        query_function (callable): The main query logic. It must accept a session as its first argument.
        *args: Positional arguments to pass to `query_function`.
        on_complete (callable, optional): A callback executed on successful query completion. Receives the result.
        on_error (callable, optional): A callback executed if an exception occurs. Receives the exception.
        on_finally (callable, optional): A callback executed at the end, regardless of success or failure.
        **kwargs: Keyword arguments to pass to `query_function`.

    Returns:
        Any: The result of the query function if successful, otherwise `None`.

    Raises:
        Exception: Re-raises any exception unless handled in `on_error`.

    Example:
        def query_function(session, *args, **kwargs):
            return session.query(User).filter_by(id=1).first()

        def on_complete(result):
            print(f"Query result: {result}")

        def on_error(error):
            print(f"An error occurred: {error}")

        session_factory = create_session
        safe_execute(session_factory, query_function, on_complete=on_complete, on_error=on_error)
    """
    session = session_factory()  # Create a session
    try:
        # Execute the query and commit if no exceptions occur
        result = query_function(session, *args, **kwargs)
        session.commit()

        # Invoke on_complete callback if provided
        if on_complete:
            on_complete(result)

        return result

    except SQLAlchemyError as e:
        session.rollback()  # Rollback the transaction on exception

        # Invoke on_error callback if provided
        if on_error:
            on_error(e)
        else:
            raise e  # Re-raise the exception if no error handlers is specified

    finally:
        # Always invoke on_finally callback if provided
        if on_finally:
            on_finally()

        session.close()  # Ensure the session is closed


def scoped_execute(
    session_factory,
    query_function,
    *args,
    on_complete=None,
    handle_error=None,
    on_finally=None,
    **kwargs
):
    """
    Execute a query in a database session with scoped error and resource handling.

    Args:
        session_factory: A callable or object providing a database session (ScopedSession or Session).
        query_function: Function that executes the query, taking the session as the first argument.
        on_complete: Callback for successful execution, receives the result.
        handle_error: Callback for handling errors, receives the error object.
        on_finally: Callback for cleanup operations, called in the finally block.
        *args, **kwargs: Additional arguments passed to the query function.

    Returns:
        The result of the query function, if successful.
    """
    # Create or retrieve a session
    session = session_factory() if callable(session_factory) else session_factory

    try:
        # Execute the query
        query_result = query_function(session, *args, **kwargs)
        # Check for query errors
        if hasattr(query_result, 'data') and query_result.data is None:
            if handle_error:
                handle_error(query_result.error)
            return None

        # Invoke on_complete if provided
        if on_complete:
            on_complete(query_result)

        return query_result  # Return result if no on_complete

    except SQLAlchemyError as e:



        # Invoke handle_error if provided
        if handle_error:
            handle_error(e)
        else:
            raise e  # Re-raise the exception if no error handler is specified

        # Rollback transaction on error
        session.rollback()

    finally:
        # Invoke on_finally if provided
        if on_finally:
            on_finally()

        # Cleanup session (remove for ScopedSession, close otherwise)
        if hasattr(session, "remove"):  # ScopedSession
            session.remove()
        else:  # Regular Session
            session.close()


def http_handle_error(query_error: QueryResultError | str ):
    """Handle errors by raising an HTTPException."""

    #print(f"Query error: {query_error}")
    if isinstance(query_error, QueryResultError):
        error_map = {
            QueryResultErrorType.NOT_FOUND: (404, query_error.message),
            QueryResultErrorType.INVALID_REQUEST: (400, query_error.message),
            QueryResultErrorType.DATABASE_ERROR: (500, query_error.message),
            QueryResultErrorType.UNKNOWN_ERROR: (500, query_error.message),
        }
        status_code, detail = error_map.get(
            query_error.error_type, (500, "An unexpected error occurred")
        )
        raise HTTPException(status_code=status_code, detail=str(detail))

    raise HTTPException(status_code=500, detail=str(query_error))




from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

async def scoped_execute_async(
        session_factory,
        query_function,
        *args,
        on_complete=None,
        handle_http_error=None,
        on_finally=None,
        **kwargs
):
    """
    Asynchronously execute a query in a database session with scoped error and resource handling.

    Args:
        session_factory: A callable or object providing an async database session (e.g., AsyncSession).
        query_function: Coroutine that executes the query, taking the session as the first argument.
        on_complete: Callback for successful execution, receives the result.
        handle_http_error: Callback for handling errors, receives the error object.
        on_finally: Callback for cleanup operations, called in the finally block.
        *args, **kwargs: Additional arguments passed to the query function.

    Returns:
        The result of the query function, if successful.
    """
    # Create or retrieve a session
    session = session_factory

    try:
        # Execute the query function and await the result
        query_result = await query_function(session, *args, **kwargs)

        # Invoke on_complete if provided
        if on_complete:
            on_complete(query_result)

        return query_result  # Return result if no on_complete

    except SQLAlchemyError as e:
        # Invoke handle_error if provided
        if handle_http_error:
            handle_http_error(e)
        else:
            raise e  # Re-raise the exception if no error handler is specified

        # Rollback transaction on error
        session.rollback()

    finally:
        # Invoke on_finally if provided
        if on_finally:
            on_finally()

        # Cleanup session (remove for ScopedSession, close otherwise)
        if hasattr(session, "remove"):  # ScopedSession
            session.remove()
        else:  # AsyncSession
            session.close()
