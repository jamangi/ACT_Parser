import os
from pathlib import Path

LOG_FOLDER = Path.home() / 'AppData' / 'Roaming' / 'Advanced Combat Tracker' / 'FFXIVLogs'
USER = "Rasp"  # or Grey
CODES = {
    "108739E2": "Irrelevant Movement",
    "000E": "Party",
    "001D": "Emote",
    "000D": f"Tell from Person to {USER}",
    "000C": f"Tell from {USER} to Person",
    "000B": "Shout",
    "001E": "Yell",
    "000A": "Say"
}


def get_logs(log_folder):
    folder_path = Path(log_folder)
    return [file for file in folder_path.iterdir() if file.is_file()]


def get_most_recent_log(list_of_files):
    return max(list_of_files, key=os.path.getmtime)


def get_log_text(log_file):
    with open(log_file, "r", encoding="utf8") as log:
        return log.read()


async def get_last_post(client, message):

    # Get the text of the last update to the log, split into lines
    post_history = [msg async for msg in message.channel.history(limit=25) if msg.author == client.user and msg.content.split('\n')[-1] == '--END LOG--']
    if len(post_history) == 0:  # If there are no log files in the last 25 messages, generate whole log
        last_post = ''
    else:
        last_post = post_history[0].content
    last_post_lines = last_post.split('\n')
    del last_post_lines[-1]

    return last_post_lines


def do_we_have_all_needed_logs(last_post_lines, logs):
    # Check whether the last few lines are in this logs file
    if len(last_post_lines) > 0 and last_post_lines[-1].split('): ', 1)[-1] in logs:  # Make sure this is applicable
        for line in last_post_lines[-10:]:
            line_text = line.split('): ', 1)[1]  # Eliminate character name from line
            if line_text not in logs:
                return False
    return True


def find_where_to_start(lines, logs):
    # Isolate the part of the logs text that comes after the last lines
    for line in lines[-10:]:
        line_text = line.split('): ', 1)[1]  # Eliminate character name from line
        logs = logs.split(line_text, 1)[-1]  # Check for the first instance of the last ten lines.
    return logs


def parse_new_session(new_logs):

    # Identify messages
    separator = 'abcx separator xcba'
    new_logs = new_logs.replace('|000C|Raspberry Kitten|', f'{separator}Grey (tell): ')
    new_logs = new_logs.replace('|000D|Raspberry Kitten|', f'{separator}Rasp (tell): ')
    new_logs = new_logs.replace('|000C|Lyonette Shivertail|', f'{separator}Rasp (tell): ')
    new_logs = new_logs.replace('|000D|Lyonette Shivertail|', f'{separator}Grey (tell): ')
    new_logs = new_logs.replace('|000A|Lyonette Shivertail|', f'{separator}Grey (say): ')
    new_logs = new_logs.replace('|000A|Raspberry Kitten|', f'{separator}Rasp (say): ')
    new_logs = new_logs.replace('Lyonette Shivertail|', f'{separator}Grey (party): ')
    new_logs = new_logs.replace('Raspberry Kitten|', f'{separator}Rasp (party): ')
    messages = new_logs.split(separator)

    # Chop off extraneous log text
    messages = [message.split('|')[0] for message in messages]

    return messages


def split_into_chunks(messages):
    messages_split = []
    current_message = ''
    for message in messages:
        if len(message) + len(current_message) >= 1990:
            messages_split.append(current_message)
            current_message = message
        else:
            current_message = current_message + '\n' + message
    current_message = current_message + '\n--END LOG--'
    messages_split.append(current_message)
    return messages_split


async def ffxivparse(client, message):
    found_all_new_logs = False
    lines_in_last_update = await get_last_post(client, message)
    new_logs = ''
    history_state = 0
    while not found_all_new_logs:
        logfile_text = get_logs(history_state)
        new_logs = logfile_text + new_logs
        found_all_new_logs = do_we_have_all_needed_logs(lines_in_last_update, new_logs)
        history_state += 1
    new_logs = find_where_to_start(lines_in_last_update, new_logs)
    if 'Raspberry Kitten|' not in new_logs:
        return ['Logs are up to date! :)']
    messages = parse_new_session(new_logs)
    messages_split = split_into_chunks(messages)
    return messages_split

if __name__ == '__main__':
    print(LOG_FOLDER)
