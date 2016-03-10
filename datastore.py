import os
from settings import *

class DataStore:

    def __init__(self, storetype='flatfile'):
        self.new_listings = []
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


    def save_entry(self,datapid='None',url='None', title='None'):
        c = sqlite3.connect(self.db_path)
        check_for_listing_sql = """
            select count(post_id)
            from listings
            where
              post_id = ?
              -- AND url = ?
              -- AND title = ?;
        """

        insert_listing = """
            insert into listings values (?, ?, ?);
        """

        entry_tuple = (datapid, url, title,)

        res = c.execute(check_for_listing_sql, (datapid,))#entry_tuple)

        conteo = 0
        for row in res:
            conteo = int(row[0])

        if conteo == 0:
            c.execute(insert_listing, entry_tuple)
            c.commit()
            self.new_listings.append(entry_tuple)

        # print "Result of query: {0}".format(res[0])
