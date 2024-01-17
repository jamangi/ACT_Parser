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
