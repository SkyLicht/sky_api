from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./sky_db.db"  # SQLite database URL

Base = declarative_base()
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class DBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.engine = create_engine(
            DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
        )
        Base.metadata.create_all(bind=self.engine)
        print('Database initialized')
        self.Session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
    def get_session(self):
        return self.Session()

# Dependency to get DB session
def get_db_session():
    db = DBConnection().get_session()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()  # Rollback any active transaction if there's an error
        raise e
    finally:
        db.close()