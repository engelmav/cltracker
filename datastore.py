import os
from settings import *

class DataStore:

    def __init__(self, storetype='flatfile'):
        if storetype is 'flatfile':
            self.filestore = True
        elif storetype is 'sql':
            global sqlite3
            import sqlite3
            self.db_path = os.path.join(PROG_DIR, DB_NAME)
            self.setup_database()
        else:
            raise RuntimeError('Unknown storetype %s') % storetype


    def setup_database(self):
        if not os.path.isfile(self.db_path):
            self.create_schema()

    def create_schema(self):

        create_schema_sql = """
            create table if not exists listings (
              post_id
              , url
              , title
            );
        """
        c = sqlite3.connect(self.db_path)
        c.execute(create_schema_sql)









