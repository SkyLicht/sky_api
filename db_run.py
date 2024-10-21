from core.db.database import DBConnection
from core.data.models.hour_by_hour import HourByHour

def main():
    print('Hello World')
    db = DBConnection()
    session = db.get_session()
    print('Session:', session)

    # result = session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hour_by_hour';")
    # table_exists = result.fetchone() is not None
    #
    # print(f"Table 'hour_by_hour' exists: {table_exists}")
    pass

if __name__ == '__main__':
    main()