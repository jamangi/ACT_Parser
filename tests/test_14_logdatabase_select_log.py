from log_saver import LogDatabase  # Replace with the correct import


def test_select_log():
    # Setup: Create a LogDatabase instance
    log_db = LogDatabase(":memory:")
    log_db.create_logs_table()

    # Insert test data
    test_data = [
        {
            'datetime': '2023-12-20T15:34:54',
            'timezone': '-06:00',
            'datetime_cst': '2023-12-20T09:34:54',
            'channel_code': '000C',
            'channel': 'Tell to Ussoo Ku',
            'author': 'Ussoo Ku',
            'content': "I've chatting a lot of ppl, and not everyone is a chatter",
        },
        # Add more test data as needed
        {
            'datetime': '2023-12-20T15:34:55',
            'timezone': '-05:00',
            'datetime_cst': '2023-12-20T10:34:55',
            'channel_code': '000C',
            'channel': 'Tell to Ussoo Ku',
            'author': 'Ussoo Ku',
            'content': "lel",
        }
    ]

    for data in test_data:
        log_db.insert_log(**data)

    # Test: Select data using select_log method with filter criteria
    filter_criteria = {
        'datetime': ['2023-12-20T15:34:54'],
        'author': ['Ussoo Ku'],
        'content': ["I've chatting a lot of ppl, and not everyone is a chatter"],
    }

    selected_data = log_db.select_log(filter_criteria)

    # Verify the selected data matches the expected results
    assert len(selected_data) == 1
    assert selected_data[0]['datetime'] == '2023-12-20T15:34:54'
    assert selected_data[0]['author'] == 'Ussoo Ku'
    assert selected_data[0]['content'] == "I've chatting a lot of ppl, and not everyone is a chatter"


def test_select_log_multiple_matches():
    # Setup: Create a LogDatabase instance
    log_db = LogDatabase(":memory:")
    log_db.create_logs_table()

    # Insert test data
    test_data = [
        {
            'datetime': '2023-12-20T15:34:54',
            'timezone': '-06:00',
            'datetime_cst': '2023-12-20T09:34:54',
            'channel_code': '000C',
            'channel': 'Haltise El Yokade tells Ussoo Ku',
            'author': 'Haltise El Yokade',
            'content': "I've chatting a lot of ppl, and not everyone is a chatter",
        },
        {
            'datetime': '2023-12-20T15:34:55',
            'timezone': '-05:00',
            'datetime_cst': '2023-12-20T10:34:55',
            'channel_code': '000D',
            'channel': 'Ussoo Ku tells Haltise El Yokade',
            'author': 'Ussoo Ku',
            'content': "lel",
        },
        {
            'datetime': '2023-12-20T15:34:56',
            'timezone': '-06:00',
            'datetime_cst': '2023-12-20T09:34:56',
            'channel_code': '000D',
            'channel': 'Ussoo Ku tells Haltise El Yokade',
            'author': 'Ussoo Ku',
            'content': "Another message",
        }
    ]

    for data in test_data:
        log_db.insert_log(**data)

    # Test: Select data using select_log method with filter criteria
    filter_criteria = {
        'author': ['Ussoo Ku'],
    }

    selected_data = log_db.select_log(filter_criteria)

    # Verify the selected data matches the expected results
    assert len(selected_data) == 2  # All three entries have the same author
    assert set(entry['content'] for entry in selected_data) == {
        "lel",
        "Another message",
    }


def test_select_log_ordered_by_datetime_cst():
    # Setup: Create a LogDatabase instance
    log_db = LogDatabase(":memory:")
    log_db.create_logs_table()

    # Insert test data with different datetime_cst values
    test_data = [
        {
            'datetime': '2023-12-20T15:34:54',
            'timezone': '-06:00',
            'datetime_cst': '2023-12-22T15:34:54',
            'channel_code': '000D',
            'channel': f'Ussoo Ku tells {LogDatabase.username}',
            'author': 'Ussoo Ku',
            'content': "I've chatting a lot of ppl, and not everyone is a chatter",
        },
        {
            'datetime': '2023-12-21T12:30:00',
            'timezone': '-05:00',
            'datetime_cst': '2023-12-20T11:30:00',
            'channel_code': '000D',
            'channel': f'Ussoo Ku tells {LogDatabase.username}',
            'author': 'Ussoo Ku',
            'content': "Another message",
        },
        {
            'datetime': '2023-12-20T18:45:22',
            'timezone': '-06:00',
            'datetime_cst': '2023-12-20T18:45:22',
            'channel_code': '001D',
            'channel': 'Emote',
            'author': 'Emote User',
            'content': "Emote content",
        },
    ]

    for data in test_data:
        log_db.insert_log(**data)

    # Test: Select data using select_log method with filter criteria
    selected_data = log_db.select_log({"author": "Ussoo Ku"}, order_by='datetime_cst')

    # Verify the selected data is ordered by datetime_cst
    assert len(selected_data) == 2
    assert selected_data[0]['datetime_cst'] == '2023-12-20T11:30:00'
    assert selected_data[1]['datetime_cst'] == '2023-12-22T15:34:54'


def test_select_log_or_functionality():
    # Setup: Create a LogDatabase instance
    log_db = LogDatabase(":memory:")
    log_db.create_logs_table()

    # Insert test data with different authors
    test_data = [
        {
            'datetime': '2023-12-20T15:34:54',
            'timezone': '-06:00',
            'datetime_cst': '2023-12-20T09:34:54',
            'channel_code': '000C',
            'channel': 'Zena tells Ussoo Ku',
            'author': 'Zena',
            'content': "Message from Zena",
        },
        {
            'datetime': '2023-12-21T12:30:00',
            'timezone': '-05:00',
            'datetime_cst': '2023-12-21T10:30:00',
            'channel_code': '000C',
            'channel': 'Sota tells Ussoo Ku',
            'author': 'Sota',
            'content': "Message from Sota",
        },
        {
            'datetime': '2023-12-20T18:45:22',
            'timezone': '-06:00',
            'datetime_cst': '2023-12-20T12:45:22',
            'channel_code': '001D',
            'channel': 'Emote',
            'author': 'Emote User',
            'content': "Emote content",
        },
    ]

    for data in test_data:
        log_db.insert_log(**data)

    # Test: Select data using select_log method with 'or' functionality
    filter_criteria = {'author': ['Zena', 'Sota']}
    selected_data = log_db.select_log(filter_criteria)

    # Verify the selected data contains entries with either author Zena or Sota
    assert len(selected_data) == 2
    assert any(entry['author'] == 'Zena' for entry in selected_data)
    assert any(entry['author'] == 'Sota' for entry in selected_data)


def test_select_log_no_filter():
    # Setup: Create a LogDatabase instance
    log_db = LogDatabase(":memory:")
    log_db.create_logs_table()

    # Insert test data
    test_data = [
        {
            'datetime': '2023-12-20T15:34:54',
            'timezone': '+00:00',
            'datetime_cst': '2023-12-20T09:34:54',
            'channel_code': '000C',
            'channel': 'Tell to Ussoo Ku',
            'author': 'Ussoo Ku',
            'content': "Message from Ussoo Ku",
        },
        {
            'datetime': '2023-12-21T12:30:00',
            'timezone': '-04:00',
            'datetime_cst': '2023-12-21T10:30:00',
            'channel_code': '000D',
            'channel': 'Tell to Zena',
            'author': 'Zena',
            'content': "Message from Zena",
        },
        {
            'datetime': '2023-12-20T18:45:22',
            'timezone': '-05:00',
            'datetime_cst': '2023-12-20T17:45:22',
            'channel_code': '001D',
            'channel': 'Emote',
            'author': 'Emote User',
            'content': "Emote content",
        },
    ]

    for data in test_data:
        log_db.insert_log(**data)

    # Test: Select data using select_log method with no filter
    selected_data_no_filter = log_db.select_log()
    assert len(selected_data_no_filter) == 0

    # Test: Select data using select_log method with an empty filter
    selected_data_empty_filter = log_db.select_log({})
    assert len(selected_data_empty_filter) == 0
    assert selected_data_empty_filter == []


def test_select_by_date_range():
    # Setup: Create a LogDatabase instance
    log_db = LogDatabase(":memory:")
    log_db.create_logs_table()

    # Insert test data
    test_data = [
        {
            'datetime': '2023-12-20T15:34:54',
            'timezone': '-00:00',
            'datetime_cst': '2023-12-20T09:34:54',
            'channel_code': '000C',
            'channel': 'Tell to Ussoo Ku',
            'author': 'Ussoo Ku',
            'content': "Message from Ussoo Ku",
        },
        {
            'datetime': '2023-12-21T12:30:00',
            'timezone': '-04:00',
            'datetime_cst': '2023-12-21T10:30:00',
            'channel_code': '000D',
            'channel': 'Tell to Zena',
            'author': 'Zena',
            'content': "Message from Zena",
        },
        {
            'datetime': '2023-12-20T18:45:22',
            'timezone': '-00:00',
            'datetime_cst': '2023-12-20T12:45:22',
            'channel_code': '001D',
            'channel': 'Emote',
            'author': 'Emote User',
            'content': "Emote content",
        },
    ]

    for data in test_data:
        log_db.insert_log(**data)

    # Test: Select data using select_by_date method with date range filter
    start_datetime_cst = '2023-12-20T10:00:00'
    end_datetime_cst = '2023-12-21T11:00:00'

    selected_data_within_range = log_db.select_log(
        start_datetime_cst=start_datetime_cst,
        end_datetime_cst=end_datetime_cst
    )

    assert len(selected_data_within_range) == 2
    assert selected_data_within_range[0]['datetime_cst'] == '2023-12-20T09:34:54'
    assert selected_data_within_range[1]['datetime_cst'] == '2023-12-20T12:45:22'


def test_select_by_date_order():
    # Setup: Create a LogDatabase instance
    log_db = LogDatabase(":memory:")
    log_db.create_logs_table()

    # Insert test data
    test_data = [
        {
            'datetime': '2023-12-20T15:34:54',
            'timezone': '-06:00',
            'datetime_cst': '2023-12-20T09:34:54',
            'channel_code': '000C',
            'channel': 'Tell to Ussoo Ku',
            'author': 'Ussoo Ku',
            'content': "Message from Ussoo Ku",
        },
        {
            'datetime': '2023-12-21T12:30:00',
            'timezone': '-05:00',
            'datetime_cst': '2023-12-21T10:30:00',
            'channel_code': '000D',
            'channel': 'Tell to Zena',
            'author': 'Zena',
            'content': "Message from Zena",
        },
        {
            'datetime': '2023-12-20T18:45:22',
            'timezone': '-06:00',
            'datetime_cst': '2023-12-20T12:45:22',
            'channel_code': '001D',
            'channel': 'Emote',
            'author': 'Emote User',
            'content': "Emote content",
        },
    ]

    for data in test_data:
        log_db.insert_log(**data)

    # Test: Select data using select_by_date method and check ordering
    start_datetime_cst = '2023-12-20T00:00:00'
    end_datetime_cst = '2023-12-22T00:00:00'

    selected_data_ordered = log_db.select_log(
        start_datetime_cst=start_datetime_cst,
        end_datetime_cst=end_datetime_cst
    )

    # Ensure the results are ordered by datetime_cst
    assert all(
        selected_data_ordered[i]['datetime_cst'] <= selected_data_ordered[i + 1]['datetime_cst']
        for i in range(len(selected_data_ordered) - 1)
    )


def test_select_by_date_with_filter_intermediate():
    # Setup: Create a LogDatabase instance
    log_db = LogDatabase(":memory:")
    log_db.create_logs_table()

    # Insert test data
    test_data = [
        {'datetime_cst': '2023-12-20T15:34:54', 'author': 'User1', 'content': 'Message 1'},
        {'datetime_cst': '2023-12-20T15:35:00', 'author': 'User2', 'content': 'Message 2'},
        {'datetime_cst': '2023-12-20T18:00:00', 'author': 'User1', 'content': 'Message 3'},
        {'datetime_cst': '2023-12-20T17:00:00', 'author': 'User2', 'content': 'Message 4'},
    ]

    for data in test_data:
        log_db.insert_log(**data)

    # Define datetime_cst range
    start_datetime_cst = '2023-12-20T15:00:00'
    end_datetime_cst = '2023-12-20T17:30:00'

    # Test: Select data using select_by_date method with filter criteria
    filter_criteria = {'author': ['User1']}
    selected_data_filtered = log_db.select_log(
        start_datetime_cst=start_datetime_cst,
        end_datetime_cst=end_datetime_cst,
        filter=filter_criteria
    )

    # Ensure the filter is applied to the result set
    assert all(entry['author'] == 'User1' for entry in selected_data_filtered)
    assert len(selected_data_filtered) == 1


def test_select_log_channel_filter():
    # Setup: Create a LogDatabase instance
    log_db = LogDatabase(":memory:")
    log_db.create_logs_table()

    # Insert test data with different channels
    test_data = [
        {
            'datetime': '2023-12-20T15:34:54',
            'timezone': '-06:00',
            'datetime_cst': '2023-12-20T09:34:54',
            'channel_code': '000D',
            'channel': 'Zena tells Ussoo Ku',
            'author': 'Ussoo Ku',
            'content': "Message from Ussoo Ku",
        },
        {
            'datetime': '2023-12-21T12:30:00',
            'timezone': '-05:00',
            'datetime_cst': '2023-12-21T10:30:00',
            'channel_code': '000C',
            'channel': 'Haltise tells Lyon',
            'author': 'Haltise',
            'content': "Message from Haltise",
        },
        {
            'datetime': '2023-12-20T18:45:22',
            'timezone': '-06:00',
            'datetime_cst': '2023-12-20T12:45:22',
            'channel_code': '000E',
            'channel': 'Party',
            'author': 'Party User',
            'content': "Party content",
        },
        {
            'datetime': '2023-12-20T21:00:00',
            'timezone': '-06:00',
            'datetime_cst': '2023-12-20T15:00:00',
            'channel_code': '000A',
            'channel': 'Say',
            'author': 'Say User',
            'content': "Say something",
        },
        {
            'datetime': '2023-12-21T08:15:00',
            'timezone': '-05:00',
            'datetime_cst': '2023-12-21T06:15:00',
            'channel_code': '000B',
            'channel': 'Shout',
            'author': 'Shout User',
            'content': "Shout it out",
        },
    ]

    for data in test_data:
        log_db.insert_log(**data)

    # Test: Select data using select_log method with 'channel' filter criteria
    filter_criteria = {'channel': ['Party', 'Tell', 'Say']}
    selected_data = log_db.select_log(filter_criteria)

    # Verify the selected data contains entries with channels matching the criteria
    assert len(selected_data) == 3
    assert all(entry['channel'] in filter_criteria['channel'] for entry in selected_data)

    # Verify that entries with channels not in the criteria are not included
    assert all(entry['channel'] not in ('Unknown', 'Shout') for entry in selected_data)


def test_select_log_channel_filter_2():
    # Setup: Create a LogDatabase instance
    log_db = LogDatabase(":memory:")
    log_db.create_logs_table()

    # Insert test data with different channels
    test_data = [
        {
            'datetime': '2023-12-20T15:34:54',
            'timezone': '-06:00',
            'datetime_cst': '2023-12-20T09:34:54',
            'channel_code': '000D',
            'channel': 'Sayaman tells Ussoo Ku',
            'author': 'Ussoo Ku',
            'content': "Message from Ussoo Ku",
        },
        {
            'datetime': '2023-12-21T12:30:00',
            'timezone': '-05:00',
            'datetime_cst': '2023-12-21T10:30:00',
            'channel_code': '000C',
            'channel': 'Party tells Lyon',
            'author': 'Party',
            'content': "Message from Party",
        },
        {
            'datetime': '2023-12-20T18:45:22',
            'timezone': '-06:00',
            'datetime_cst': '2023-12-20T12:45:22',
            'channel_code': '000E',
            'channel': 'Party',
            'author': 'Party User',
            'content': "Party content",
        },
        {
            'datetime': '2023-12-20T21:00:00',
            'timezone': '-06:00',
            'datetime_cst': '2023-12-20T15:00:00',
            'channel_code': '000A',
            'channel': 'Say',
            'author': 'Say User',
            'content': "Say something",
        },
        {
            'datetime': '2023-12-21T08:15:00',
            'timezone': '-05:00',
            'datetime_cst': '2023-12-21T06:15:00',
            'channel_code': '000B',
            'channel': 'Shout',
            'author': 'Shout User',
            'content': "Shout it out",
        },
    ]

    for data in test_data:
        log_db.insert_log(**data)

    # Test: Select data using select_log method with 'channel' filter criteria
    filter_criteria = {'channel': ['Party', 'Say']}
    selected_data = log_db.select_log(filter_criteria)

    # Verify the selected data contains entries with channels matching the criteria
    assert len(selected_data) == 2
    assert all(entry['channel'] in filter_criteria['channel'] for entry in selected_data)

    # Verify that entries with channels not in the criteria are not included
    assert all(entry['channel'] not in ('Unknown', 'Shout',
                                        'Sayaman tells Ussoo Ku', 'Party tells Lyon') for entry in selected_data)
