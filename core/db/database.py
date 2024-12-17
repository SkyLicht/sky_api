from sqlalchemy import create_engine, event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

# Define the database URL - using SQLite with a local file named `sky_db.db`.
DATABASE_URL = "sqlite:///./sky_db.db"


# Base class for defining ORM models.
Base = declarative_base()

class DBConnection:
    """
    Singleton class to manage database connection and session factories.
    Ensures only one database connection exists and provides thread-safe sessions.
    """
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls):
        # Singleton pattern: create only one instance of this class
        if cls._instance is None:
            cls._instance = super(DBConnection, cls).__new__(cls)
            cls._instance._initialize()  # Initialize the instance
        return cls._instance

    def _initialize(self):
        """
        Initialize the database engine, create tables, and setup session factories.
        """
        self.engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},  # Required for SQLite in multi-threaded apps
            echo=False
        )

        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON;")
            cursor.close()



        Base.metadata.create_all(bind=self.engine)

        # Create a session factory
        self.SessionFactory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False
        )

        # Create a thread-safe scoped session
        self.ScopedSession = scoped_session(self.SessionFactory)



    def create_table(self, model):
        """
        Create a specific table in the database.

        Args:
            model (Base): SQLAlchemy ORM model class that inherits from Base.

        Example:
            class ExampleModel(Base):
                __tablename__ = 'example'
                id = Column(Integer, primary_key=True)
                name = Column(String)

            DBConnection().create_table(ExampleModel)
        """
        try:
            model.metadata.create_all(self.engine)  # Create the table for the provided model
            print(f"Table for model '{model.__tablename__}' created successfully.")
        except SQLAlchemyError as e:
            print(f"Error creating table for model '{model.__tablename__}': {e}")

    def get_session(self):
        """
        Create and return a new database session.

        **Use Case**:
        - When you need a standalone database session for a single-threaded environment.
        - Example: Using in a script for bulk data processing or data migration.

        Example:
            with DBConnection().get_session() as session:
                session.add(new_object)
                session.commit()
        """
        return self.SessionFactory()

    def get_scoped_session(self):
        """
        Get a thread-safe scoped session.

        **Use Case**:
        - For use in multi-threaded applications or web frameworks where each thread requires its own session.
        - Example: Flask or FastAPI applications with multiple simultaneous requests.

        Example:
            session = DBConnection().get_scoped_session()
            session.query(Model).filter_by(id=1).first()
        """
        return self.ScopedSession


def get_db_session():
    db = DBConnection().get_session()  # Create a new session
    try:
        yield db  # Provide the session to the caller
    except SQLAlchemyError as e:
        db.rollback()  # Rollback transaction in case of an exception
        raise e  # Re-raise the exception
    finally:
        db.close()  # Always close the session


def get_scoped_db_session():
    db = DBConnection().ScopedSession  # Get the ScopedSession instance

    try:
        yield db  # Provide the session to the caller
    except SQLAlchemyError as e:
        db.rollback()  # Rollback transaction in case of an exception
        raise e  # Re-raise the exception
    finally:
        db.remove()  # Call remove() to clear the thread-local session

