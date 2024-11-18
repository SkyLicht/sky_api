import argparse

from core.db.database import DBConnection
from core.data.models.hour_by_hour import HourByHour
from core.data.models.user_model import User, Role, Permission

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



def init_db():
    db = DBConnection()
    session = db.get_session()
    print('Session:', session)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= 'Manage database')
    parser.add_argument(
        '--db',
        type= str,
        choices=['init','show_data'],
        help= '...'
    )

    arg = parser.parse_args()

    if arg.db == 'init':
        init_db()
