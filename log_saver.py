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
    username = config("FF_USERNAME", default="Haltise El Yokade")  # default is for testing

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)

    @staticmethod
    def code_to_channel(other_user="nobody", code="nothing"):
        """Retrieves and returns a descriptive label for a given channel code.

        Parameters:
        - code (str): The channel code to be looked up.
        - other_user (str): The username of the other user involved in the channel communication.

        Returns:
        str: A descriptive label corresponding to the input channel code, or "unrecognized" if the code is not found."""

        CHANNEL_CODES = {
            "000E": "Party",
            "001D": "Emote",
            "003C": "Error Message",
            "000D": f"{other_user} tells {LogDatabase.username}",
            "000C": f"{LogDatabase.username} tells {other_user}",
            "000B": "Shout",
            "001E": "Yell",
            "000A": "Say"
        }
        if code in CHANNEL_CODES:
            return CHANNEL_CODES[code]
        else:
            return "unrecognized"

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

    @staticmethod
    def parse_log(log_text):
        """Parses a line from the logs to extract:
        1) Time in perspective time zone (not necessarily CST)
        2) Time zone in hours from GMT
        3) Channel code (for example 000E for party chat)
        4) Author (or recipient if channel code is 000C, tell to)
        5) Content

        Input: str -- line of log text
        Output: 5-entry dict {str: str, str: str, str: str, str: str, str: str} -- time, time zone,
            channel code, author, and content of message
        """

        # Split logs by |
        log_list = log_text.split('|')

        # Find attributes
        time = log_list[1][:-14]  # cuts off milliseconds
        timezone = log_list[1][-6:]
        channel_code = log_list[2]
        author = log_list[3]
        content = log_list[4]

        # Create dictionary of attributes
        parsed_log = {'datetime': time, 'timezone': timezone, 'channel_code': channel_code, 'author': author, 'content': content}
        return parsed_log


# Example usage:
if __name__ == "__main__":
    # Creating an instance of LogDatabase
    log_db = LogDatabase("ffxiv_logger.db")

    # Creating the table
    log_db.create_log_file_table()
