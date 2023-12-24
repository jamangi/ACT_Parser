import os
import sqlite3


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


    def create_log_file_table(self):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    log_filename TEXT,
                    size INTEGER
                )
            ''')

# Example usage:
if __name__ == "__main__":
    # Creating an instance of LogDatabase
    log_db = LogDatabase("example_database.db")

    # Creating the table
    log_db.create_log_file_table()
