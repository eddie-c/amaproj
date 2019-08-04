from sqlitedb.db_init import *
class Sqlops(object):
    def __init__(self):
        self.session = DBSession()

    def get_session(self):
        return self.session()

