import calendar
import re
from datetime import datetime, timedelta

import log_saver


def cst_to_gmt(datetime_cst_string, hours_to_add=6):
    """Convert CST string to GMT string. Inputs and outputs should be formatted like '2023-12-17T11:59:56'."""

    # Split cst datetime string into integer components
    year, month, day, hour, minute, second = split_datetime_string(datetime_cst_string)

    # Convert to datetime format
    datetime_cst = datetime(year, month, day, hour, minute, second)

    # Apply time change
    datetime_gmt = datetime_cst + timedelta(hours=hours_to_add)

    # Convert to string
    datetime_gmt_string = log_saver.LogDatabase.time_to_string(datetime_gmt)

    return datetime_gmt_string


def date_discord_unix_converter(datetime_string, method):
    """Creates a unix timestamp from a GMT datetime formatted as a string
    
    :param datetime_string: (string) GMT datetime formatted as a string. For example: '2023-12-17T11:59:56'
    :param method: (string) the way the unix timestamp should be formatted. For example: 'f'
    :return: A unix timestamp ready to be posted into discord. For example: "<t:1695875996:f>"
    """

    # Search for letters other than capital T in the datetime string. If they exist, it's not properly formatted
    letters_besides_t = bool(re.search('[a-zA-SU-Z]', datetime_string))
    if letters_besides_t:
        raise ValueError("Invalid datetime format. You've got letters in there")

    # Make sure the method is valid. If method is not one of the ones Discord can recognize, raise a ValueError
    valid_methods = ['t', 'T', 'd', 'D', 'f', 'F', 'R']
    if method not in valid_methods:
        raise ValueError("Invalid method. Please choose either 't', 'T', 'd', 'D', 'f', 'F', or 'R'.")

    # Split gmt datetime string into integer components
    year, month, day, hour, minute, second = split_datetime_string(datetime_string)

    # Get unix time. timegm assumes input is in GMT timezone
    unix_time = calendar.timegm((year, month, day, hour, minute, second))

    # Create the unix timestamp using the unix time
    unix_timestamp = f"<t:{str(unix_time)}:{method}>"

    return unix_timestamp


def discord_spam_preparer(post_data_list):
    """Turns a list of metadata into a list of posts ready for Discord.

    :param post_data_list: (list of dicts) A list of posts. Each post is a dict containing the post's metadata.
    :return: (list of strings): A list of formatted post. Each post is ready for posting to Discord.
    """
    # Return empty lists and lists with no dicts without change
    if len(post_data_list) == 0:
        return post_data_list
    number_of_dicts = len([True for element in post_data_list if isinstance(element, dict)])
    if number_of_dicts == 0:
        return post_data_list

    post_list = post_data_list.copy()  # rename for easy comparison
    # Add a date marker at the beginning of the list
    init_datetime = post_list[0]['datetime_cst']
    post_list.insert(0, '# ' + date_discord_unix_converter(init_datetime, 'F'))

    for index, post_data in enumerate(post_list):
        if isinstance(post_data, dict):  # to skip date markers and continuations
            # If the next post is on a different date, add a date marker between them
            if index < len(post_list) - 1:  # Make sure it's not the last element, or index will be out of range
                this_post_datetime = post_data['datetime_cst']
                next_post_datetime = post_list[index + 1]['datetime_cst']
                if this_post_datetime.split('T')[0] != next_post_datetime.split('T')[0]:
                    post_list.insert(index + 1, '# ' + date_discord_unix_converter(next_post_datetime, 'D'))
            # Turn the metadata into a promperly formatted post
            post_string = post_constructor(post_data)
            post_list[index] = post_string
        else:
            post_string = post_data

        # Shorten any strings that are over 2000 characters long
        if len(post_string) >= 2000:
            # If the string has spaces near the cutoff, use the last space as a separator
            if ' ' in post_string[1950:1999]:
                this_post_string = post_string.rsplit(' ', 1)[0]
                overflow_post_string = "(continued)" + post_string[len(this_post_string) + 1:]
            # If there are no spaces near the cutoff, just cut it off at 1999 characters
            else:
                this_post_string = post_string[:1999]
                overflow_post_string = "(continued) " + post_string[1999:]
            post_list.insert(index + 1, overflow_post_string)
            post_list[index] = this_post_string

    return post_list


def post_constructor(post_data):
    """Creates a string formatted to present a message together with its metadata. The string includes not only the
    message's content but also a unix timestamp, the name of the person who sent the message and the channel it was
    sent in.

    :param post_data: (dict) the content and metadata for a single message. Must include the message's content plus
    author, channel, and datetime_cst metadata.
    :return: (string) a formatted post that includes all the desired metadata.
    """
    # Make sure post_data has all the metadata needed for this operation. The default KeyError isn't very informative
    required_keys = ['datetime_cst', 'author', 'channel', 'content']
    keys_present = [True for required_key in required_keys if required_key in post_data]
    if len(keys_present) < len(required_keys):
        raise KeyError("post_constructor is missing metadata! It needs data on datetime_cst, author, channel, and "
                       "content or else it can't make a post")

    # Create a unix timestamp for the message time
    datetime_gmt = cst_to_gmt(post_data['datetime_cst'])
    unix_gmt = date_discord_unix_converter(datetime_gmt, 'T')

    # Format the channel and author data (tells get different formatting)
    if post_data['author'] in post_data['channel']:
        channel_and_author = pretty_tell(post_data['channel'])
    else:
        channel_and_author = f"{post_data['channel']} - **{post_data['author']}**"

    # Format all this metadata into a post
    formatted_post = f"{unix_gmt} - {channel_and_author}: {post_data['content']}"

    return formatted_post


def pretty_tell(tell_channel):
    """Formats a tell channel metadata string so the characters involved are bolded.

    :param tell_channel: tell channel metadata. Example: 'Raspberry Kitten tells Lyonette Shivertail'
    :return: tell channel metadata but with fancy bolding. Example: '**Raspberry Kitten** tells **Lyonette Shivertail**'
    """
    tells_count = sum(tell_channel[i:].startswith(" tells ") for i in range(len(tell_channel)))
    # If there are no instances of ' tells ', just return the input as is
    if tells_count == 0:
        return tell_channel

    # Simple case where there's only one instance of ' tells '
    elif tells_count == 1:
        author, receiver = tell_channel.split(' tells ')
        bolded_tell_channel = f"**{author}** tells **{receiver}**"

    # If there's more than one instance of tells, make sure they're not in the first two words, at least
    else:
        first_two_words = ' '.join(tell_channel.split()[:2])
        after_first_two_words = ' ' + ' '.join(tell_channel.split()[2:])
        author_remainder, receiver = after_first_two_words.split(' tells ')
        author = first_two_words + author_remainder
        bolded_tell_channel = f"**{author}** tells **{receiver}**"

    return bolded_tell_channel


def post_bundler(string_list):
    """
    Concatenates a list of strings with newlines, ensuring each resulting string is nearly 2000 characters or less.

    Args:
        string_list (list of str): List of strings to concatenate.

    Returns:
        list of str: List of concatenated strings.
    """
    if not string_list or not len(string_list):
        return []
    max_length = 2000
    bundled_posts = []
    current_bundle = ""

    for string in string_list:
        # Check if adding the current string would exceed the maximum length
        if len(current_bundle) + len(string) + 1 <= max_length:
            # Add the current string to the current bundle with a newline
            current_bundle += string + "\n"
        else:
            # If adding the current string exceeds the maximum length, add the current bundle to the list
            bundled_posts.append(current_bundle.strip())  # Remove trailing newline
            # Start a new bundle with the current string
            current_bundle = string + "\n"

    # Append the last bundle to the list
    bundled_posts.append(current_bundle.strip())  # Remove trailing newline

    return bundled_posts


def split_datetime_string(datetime_string):
    """Splits a datetime string into different int variables for year, month, day, hour, minute, second.
    Accepts two formats:
    - '2023-12-17T11:59:56'
    - '2023-12-18'
    In the second case, where there's no time info, hour: minute, and second are returned as 0
    """
    # Check whether only year-month-day or also hour-minute-second are included in the datetime_string
    year, month, day, hour, minute, second = '0', '0', '0', '0', '0', '0'
    if 'T' in datetime_string:

        # Split into year, month, day, hour, minute, second.
        if not log_saver.LogDatabase.check_datetime_format(datetime_string):
            raise ValueError('Incorrect datetime format or impossible date.')
        datetime_string, hms = datetime_string.split('T')
        hour, minute, second = hms.split(':')
    year, month, day = datetime_string.split('-')

    # Turn them all into integers
    year = int(year)
    month = int(month)
    day = int(day)
    hour = int(hour)
    minute = int(minute)
    second = int(second)

    return year, month, day, hour, minute, second
