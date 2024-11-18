from multiprocessing.forkserver import connect_to_new_process


class UserDAO:
    def __init__(self, connection):
        self.conn = connect_to_new_process