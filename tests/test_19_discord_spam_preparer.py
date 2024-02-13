# test_log_util.py
from log_util import discord_spam_preparer, date_discord_unix_converter, post_constructor
import pytest


def test_discord_spam_preparer_title_check():
    # Create test data with datetime_cst values
    post_data_list = [
        {
            'datetime_cst': '2023-12-20T09:34:54',
            'channel': 'Some Channel',
            'author': 'Some Author',
            'content': 'Message 1',
        },
    ]

    result_list = discord_spam_preparer(post_data_list)

    # Check if "<t:timestamp:D>" strings are added before the appropriate entries
    assert result_list[0].startswith("# <t:")  # date of first msg post
    assert result_list[1].startswith("<t:")  # first msg post's content


def test_discord_spam_preparer_date_change_title_check():
    # Create test data with datetime_cst values
    post_data_list = [
        {
            'datetime_cst': '2023-12-20T09:34:54',
            'channel': 'Some Channel',
            'author': 'Some Author',
            'content': 'Message 1',
        },
        {
            'datetime_cst': '2023-12-21T10:30:00',
            'channel': 'Some Channel',
            'author': 'Some Author',
            'content': 'Message 3',
        },
    ]

    result_list = discord_spam_preparer(post_data_list)

    # Check if "<t:timestamp:D>" strings are added before the appropriate entries
    assert result_list[0].startswith("# <t:")  # initial date post
    assert result_list[1].startswith("<t:")  # content of first msg post
    assert result_list[2].startswith("# <t:")  # date change post
    assert result_list[3].startswith("<t:")  # content of second msg post


def test_discord_spam_preparer_first_datetime_cst():
    post_data_list = [
        {
            'datetime_cst': '2023-12-20T09:34:54',
            'channel': 'Some Channel',
            'author': 'Some Author',
            'content': 'Some Content 1',
        },
        {
            'datetime_cst': '2023-12-20T09:35:54',
            'channel': 'Some Channel',
            'author': 'Some Author',
            'content': 'Some Content 2',
        },
        {
            'datetime_cst': '2023-12-21T10:30:00',
            'channel': 'Another Channel',
            'author': 'Another Author',
            'content': 'Another Content',
        },
    ]

    result_list = discord_spam_preparer(post_data_list)

    # Check if the result_list is a list of strings
    assert isinstance(result_list, list)
    assert all(isinstance(item, str) for item in result_list)

    # Check if the first entry in result_list is as expected
    expected_first_non_title = post_constructor(post_data_list[0])
    assert result_list[1] == expected_first_non_title


def test_discord_spam_preparer_date_change_check2():
    # Create test data with datetime_cst values
    post_data_list = [
        {
            'datetime_cst': '2023-12-20T09:34:54',
            'channel': 'Some Channel',
            'author': 'Some Author',
            'content': 'Message 1',
        },
        {
            'datetime_cst': '2023-12-20T09:35:54',
            'channel': 'Some Channel',
            'author': 'Some Author',
            'content': 'Message 2',
        },
        {
            'datetime_cst': '2023-12-21T10:30:00',
            'channel': 'Some Channel',
            'author': 'Some Author',
            'content': 'Message 3',
        },
    ]

    result_list = discord_spam_preparer(post_data_list)

    # Check if "<t:timestamp:D>" strings are added before the appropriate entries
    assert result_list[0].startswith("# <t:")
    assert result_list[1].startswith("<t:")
    assert result_list[2].startswith("<t:")
    assert result_list[3].startswith("# <t:")
    assert result_list[4].startswith("<t:")


def test_discord_spam_preparer_entry_length():
    # Create test data with long content to exceed 2000 characters
    post_data_list = [
        {
            'datetime_cst': '2023-12-20T09:34:54',
            'channel': 'Some Channel',
            'author': 'Some Author',
            'content': 'A' * 2000,
        },
        {
            'datetime_cst': '2023-12-21T09:35:54',
            'channel': 'Some Channel',
            'author': 'Some Author',
            'content': 'B' * 2000,
        },
        {
            'datetime_cst': '2023-12-21T09:35:55',
            'channel': 'Some Channel',
            'author': 'Some Author',
            'content': 'End chatter'
        },
    ]

    result_list = discord_spam_preparer(post_data_list)

    assert result_list[0].startswith("# <t:")  # date start
    assert result_list[1].startswith("<t:")  # content
    assert not result_list[2].startswith("<t:")  # content continued
    assert result_list[3].startswith("# <t:")  # date change
    assert result_list[4].startswith("<t:")  # content
    assert not result_list[5].startswith("<t:")  # content continued
    assert result_list[6].startswith("<t:")  # content of next post, same day

    # Check if every entry in result_list is less than 2000 characters
    assert all(len(entry) < 2000 for entry in result_list)


def test_discord_spam_preparer_empty_list():
    # Create an empty test data list
    post_data_list = []

    result_list = discord_spam_preparer(post_data_list)

    # Check if the result list is empty
    assert len(result_list) == 0


if __name__ == "__main__":
    pytest.main()
