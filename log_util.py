import calendar

import log_saver


def date_discord_unix_converter(datetime_string, method):
    """Creates a unix timestamp from a GMT datetime formatted as a string
    
    :param datetime_string: (string) GMT datetime formatted as a string. For example: '2023-12-17T11:59:56'
    :param method: (string) the way the unix timestamp should be formatted. For example: 'f'
    :return: A unix timestamp ready to be posted into discord. For example: "<t:1695875996:f>"
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

    # Get unix time. timegm assumes input is in UTC timezone
    unix_time = calendar.timegm((year, month, day, hour, minute, second))

    # Create the unix timestamp using the unix time
    unix_timestamp = f"<t:{str(unix_time)}:{method}>"

    return unix_timestamp


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
