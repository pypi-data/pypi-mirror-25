

import psycopg2, urlparse, os



class Db_class(object):


    def __init__(self, url="DATABASE_URL"):
        urlparse.uses_netloc.append('postgres')
        if url == 'DATABASE_URL':
            self.url = urlparse.urlparse(os.environ[url])
        else:
        #     if other url was specified, for remote accessm us that and not OS values
            self.url = urlparse.urlparse(url)
        self.conn = None
        self.cursor = None


    def connect_to_db(self):
        try:
            conn = psycopg2.connect(
                database=self.url.path[1:],
                user=self.url.username,
                password=self.url.password,
                host=self.url.hostname,
                port=self.url.port
            )
            print("successful connection to db")
            self.conn = conn
            self.cursor = conn.cursor()
        except Exception as e:
            print "connect_to_db Error with: " , e


    def close_conn(self):
        try:
            self.conn.close()
            print "closed connection"
        except Exception as e:
            print 'close_conn Error with: ', e


    def close_cursor_commit_changes(self):
        self.cursor.close()
        try:
            self.conn.commit()
            print 'Commited changes'
        except Exception as e:
            print 'close_cursor_commit_changes Error with: ', e


    def create_table(self, name, columns_list):
        self.connect_to_db()
        columns = ', '.join("{} {}".format(k,v) for k,v in columns_list)
        table_command = """CREATE TABLE {} ({});""".format(name, columns)
        try:
            self.cursor.execute(table_command)
            print 'created table'
        except Exception as e:
            print 'create_table Error with: ', e
        self.close_cursor_commit_changes()
        self.close_conn()


    def drop_table(self, name):
        self.connect_to_db()
        command = """DROP TABLE {}""".format(name)
        try:
            self.cursor.execute(command)
            print 'dropped table'
        except Exception as e:
            print 'drop_table Error with: ', e
        self.close_cursor_commit_changes()
        self.close_conn()


    def list_tables(self):
        # TODO: Method not working. Bad command
        command = """SELECT * FROM information_schema.tables;"""
        try:
            self.cursor.execute(command)
        except Exception as e:
            print 'list_tables Error with: ', e


    def write_to_table(self, table_name, columns_names, values):
        self.connect_to_db()
        command = """INSERT INTO {} ({}) VALUES ({});""".format(table_name, columns_names, values)
        print command
        try:
            self.cursor.execute(command)
            print 'Successful writing to table'
        except Exception as e:
            print 'write_to_table Error with: ', e
        self.close_cursor_commit_changes()
        self.close_conn()


    def print_table(self, name):
        self.connect_to_db()
        command = """SELECT * FROM {};""".format(name)
        try:
            self.cursor.execute(command)
            print self.cursor.fetchall()
        except Exception as e:
            print 'print_table Error with: ', e
        self.close_cursor_commit_changes()
        self.close_conn()


    def delete_rows(self, table_name, condition):
        self.connect_to_db()
        command = """DELETE FROM {} WHERE {}""".format(table_name, condition)
        try:
            self.cursor.execute(command)
            print 'deleted row'
        except Exception as e:
            print 'delete_table Error with: ', e
        self.close_cursor_commit_changes()
        self.close_conn()


    def free_query(self, command):
        self.connect_to_db()
        try:
            self.cursor.execute(command)
            data = self.cursor.fetchall()
            print 'Executed command'
        except Exception as e:
            print 'free_query Error with: ', e
            data = None
        self.close_cursor_commit_changes()
        self.close_conn()

        return data

