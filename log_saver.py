import os
import sqlite3
from decouple import config
from datetime import datetime, timedelta


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
    def add_channel(log_dict, other_user=None):
        """
        Add channel information to the log metadata dictionary.

        Parameters:
        - log_dict (dict): The log dictionary to which channel information will be added.
        - other_user (str, optional): The name of the other user involved in a tell. Needed only for tells.

        Raises:
        - ValueError: If `other_user` is not provided when the channel code is '000C' or '000D'.

        Returns:
        dict: The updated log dictionary with the 'channel' key added.

        Note:
        The channel information is determined based on the channel code in the log dictionary.
        """
        code = log_dict['channel_code']
        if not other_user and (code == '000C' or code == '000D'):
            raise ValueError("Tells passed to LogDatabase.add_channel must be accompanied by an other_user kwarg.")
        channel = LogDatabase.code_to_channel(other_user, code=code)
        log_dict['channel'] = channel
        return log_dict

    @staticmethod
    def add_datetime_cst(log_dict):
        """Add a datetime_cst key and value to the dict containing the metadata for a message. Returns the input
        dictionary with an added datetime_cst entry. CST datetime is calculated using the time_to_cst static method.
        Before conversion, the metadata's 'datetime' entry (representing the local datetime for the perspective user)
        is checked to see if it exists and is formatted correctly, and the 'timezone' entry (representing the
        perspective user's offset from GMT) is checked to make sure it exists."""
        # Find out what the local datetime and timezone were. Check to make sure they're present and formatted right.
        # Convert local datetime to datetime and timezone offset to float.
        if 'datetime' not in log_dict.keys():
            raise ValueError("Local datetime is missing from the log's metadata.")
        if not LogDatabase.check_datetime_format(log_dict['datetime']):
            raise ValueError("The local datetime in the log's metadata is formatted incorrectly.")
        local_datetime = LogDatabase.string_to_time(log_dict['datetime'])
        try:
            timezone = LogDatabase.string_to_offset_hours(log_dict['timezone'])
        except KeyError:
            raise ValueError('No timezone found in log metadata.')

        # Take the local time and find the equivalent time in CST as a string, datetime_cst
        datetime_cst_datetime = LogDatabase.time_to_cst(local_datetime, timezone)
        datetime_cst = LogDatabase.time_to_string(datetime_cst_datetime)

        # Add datetime_cst to the dict and return it
        log_dict['datetime_cst'] = datetime_cst
        return log_dict

    @staticmethod
    def check_datetime_format(time_string):
        """Checks whether a datetime string is formatted correctly. Example of a valid time: '2023-12-21T06:52:50'.
        Returns True if valid and False if not valid."""
        try:
            # Split into year, month, day, hour, minute, second. If anything fails, the string was formatted wrong
            date, time = time_string.split('T')
            year, month, day = date.split('-')
            hour, minute, second = time.split(':')

            date_len_check, time_len_check, date_num_check, time_num_check = False, False, False, False

            # Check whether each parameter has the right number of digits
            if len(year) == 4 and len(month) == 2 and len(day) == 2:
                date_len_check = True
            if len(hour) == 2 and len(minute) == 2 and len(second) == 2:
                time_len_check = True

            # Check whether the year and month are realistic:
            year_check, month_check, day_check = False, False, False
            if 2010 <= int(year) <= 2100:
                year_check = True
            if 1 <= int(month) <= 12:
                month_check = True

            # Check whether the day is realistic:
            days_in_each_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
            if 1 <= int(day) <= days_in_each_month[int(month)]:
                day_check = True
            if month == '02' and day == '29' and int(year) % 4 == 0:  # February 29th valid only on leap years
                day_check = True

            if year_check and month_check and day_check:
                date_num_check = True

            # Check whether the time entries are realistic:
            hour_check, minute_check, second_check = False, False, False
            if 0 <= int(hour) <= 23:
                hour_check = True
            if 0 <= int(minute) <= 59:
                minute_check = True
            if 0 <= int(second) <= 59:
                second_check = True
            if hour_check and minute_check and second_check:
                time_num_check = True
        except ValueError:
            return False

        # Return True if all tests were passed. Return False otherwise
        if date_len_check and time_len_check and date_num_check and time_num_check:
            return True
        else:
            return False

    @staticmethod
    def code_to_channel(other_user="nobody", code="nothing"):
        """Retrieves and returns the name of the channel corresponding to a given channel code.

        Parameters:
        - code (str): The channel code to be looked up.
        - other_user (str): The username of the other user involved in the channel communication.

        Returns:
        str: The channel name corresponding to the input channel code, or "unrecognized" if the code is not found."""

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
    def fix_author(log_dict):
        """For when the message is a tell from the perspective user to another user: Changes the 'author' in the
        message log metadata to the perspective user's username"""
        if 'channel_code' not in log_dict.keys():
            return log_dict
        if log_dict['channel_code'] == '000C':
            log_dict['author'] = LogDatabase.username
        return log_dict

    @staticmethod
    def fix_log(act_log_dict):
        """Adds information to the metadata for a message obtained from the ACT logs. This is to make the information
        more immediately relevant to humans. The changes are as follows:
        - Add cst_datetime, datetime converted to CST for easy standardization
        - Put channel information in human terms
        - Adjust author metadata so that it always corresponds to the person who sent the message

        Input: Metadata from the ACT log as parsed by parse_log

        Output: The same metadata with more info as described above"""

        # Add 'datetime_cst', the datetime in CST, to the dict
        log_dict = LogDatabase.add_datetime_cst(act_log_dict)

        # Add channel, the human-readable channel info, to the dict
        if log_dict['channel_code'] == '000C' or log_dict['channel_code'] == '000D':
            other_user = log_dict['author']
        else:
            other_user = None
        log_dict = LogDatabase.add_channel(log_dict, other_user)

        # Fix author information to match sender in the case where the perspective character sends a tell
        log_dict = LogDatabase.fix_author(log_dict)

        return log_dict

    @staticmethod
    def offset_hours_to_string(offset_hours):
        """Takes a float timezone hour offset and converts it to a string. For example, -6.5 becomes '-06:30'."""
        # Split full hours from minutes
        offset_full_hours = int(offset_hours)
        offset_minutes_decimal = offset_hours - offset_full_hours

        # Convert hours to string. Make sure the hours have a 0 in front if they're single-digit and a + if positive
        offset_full_hours_string = str(offset_full_hours)
        if -10 < offset_full_hours < 10:
            offset_full_hours_string = offset_full_hours_string[:-1] + '0' + offset_full_hours_string[-1]
        if offset_hours > 0:
            offset_full_hours_string = '+' + offset_full_hours_string

        # Convert minutes to string. Make sure it's two-digit
        offset_minutes = int(abs(offset_minutes_decimal * 60))
        offset_minutes_rounded = round(offset_minutes, -1)
        offset_minutes_string = str(offset_minutes_rounded)
        if len(offset_minutes_string) < 2:
            offset_minutes_string += '0'

        # Join strings and return full timezone offset string
        offset_hours_string = offset_full_hours_string + ':' + offset_minutes_string
        return offset_hours_string

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

    @staticmethod
    def string_to_offset_hours(input_string):
        """Takes a string time zone formatted like '-06:30' and converts it to a float number of hours, in this case
        -6.5"""
        # Split full hours (before the :) from minutes (after the :). Minutes need to be converted to decimal
        offset_full_hours, offset_minutes = input_string.split(':')

        # Convert hours to int. Convert minute strings to decimal, for example '30' to .5
        offset_full_hours = int(offset_full_hours)
        offset_minutes_decimal = int(offset_minutes)/60

        # Add minutes to offset now that they've been converted to be compatible
        offset_hours = 0
        if offset_full_hours >= 0:
            offset_hours = offset_full_hours + offset_minutes_decimal
        elif offset_full_hours < 0:
            offset_hours = offset_full_hours - offset_minutes_decimal
        return offset_hours

    @staticmethod
    def string_to_time(date_string):
        """Takes string-formatted time taken from ACT log and converts it to
        datetime format so that we can do operations to account for time zones"""
        time = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
        return time

    @staticmethod
    def time_to_string(time):
        """Takes datetime-formatted time and converts it to a nice friendly string we can put wherever we want"""
        date_string = time.strftime('%Y-%m-%dT%H:%M:%S')
        return date_string

    @staticmethod
    def time_to_cst(datetime_local, offset_hours_from_gmt):
        """Convert from local time to CST time
        input: local time (datetime format), offset hours from GMT (float)
        output: time in cst (datetime format)"""
        gmt_to_cst = -6
        offset_hours_from_cst = gmt_to_cst - offset_hours_from_gmt
        datetime_cst = datetime_local + timedelta(hours=offset_hours_from_cst)
        return datetime_cst


# Example usage:
if __name__ == "__main__":
    # Creating an instance of LogDatabase
    log_db = LogDatabase("ffxiv_logger.db")

    # Creating the table
    log_db.create_log_file_table()
