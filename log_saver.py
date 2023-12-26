import os
import sqlite3
from decouple import config

def find_logfiles(string_path: str) -> (str, int):
    """
    Finds the logfiles in the given directory, which should the be ACT log folder.

    :param string_path: the path to the directory containing log files
    :return: a dictionary pairing log filenames with their size in bytes
    """

    # Find out what files are in the directory
    files_str_list = os.listdir(string_path)

    # Create a list of tuples of filenames and file sizes
    logfiles_list = [(filename, os.path.getsize(os.path.join(string_path, filename))) for filename in files_str_list]

    # Convert to dictionary
    logfiles = dict(logfiles_list)
    return logfiles


class LogDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.username = config("FF_USERNAME", default="Haltise El Yokade")  # default is for testing


    def create_log_file_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS log_files (
                log_filename TEXT,
                size INTEGER
            )
        ''')

    def create_logs_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                datetime TEXT,
                timezone TEXT,
                datetime_cst TEXT,
                author TEXT,
                channel_code TEXT,
                channel TEXT,
                content TEXT
            )
        ''')

    def __del__(self):
        if self.conn:
            self.conn.close()


# Example usage:
if __name__ == "__main__":
    # Creating an instance of LogDatabase
    log_db = LogDatabase("ffxiv_logger.db")

    # Creating the table
    log_db.create_log_file_table()
