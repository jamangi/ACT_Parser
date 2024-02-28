import interactions
from decouple import config
import git
from interactions import (slash_command, SlashContext,
                          SlashCommand, slash_option,
                          OptionType, SlashCommandChoice)
import json
from pathlib import Path
import log_saver
from log_saver import LogDatabase
from log_util import (discord_spam_preparer, date_discord_unix_converter, post_constructor,
                      post_bundler)


# Initialize your bot (replace 'YOUR_BOT_TOKEN' with your actual bot token)


DESIRED_CHANNEL_CODES = {
    "000E": "Party",
    "001D": "Emote",
    "000D": "They tell me",
    "000C": "I tell them",
    "000B": "Shout",
    "001E": "Yell",
    "000A": "Say"
}

DESIRED_CHANNELS = {
    "Party",
    "Emote",
    "Tell",
    "Shout",
    "Yell",
    "Say"
}


def update_database():
    log_counter = 0
    log_db = LogDatabase(LogDatabase.db_name)
    log_db.create_log_file_table()
    log_db.create_logs_table()
    logfiles = log_saver.find_logfiles(LogDatabase.logs_dir)  # Find logs
    loglines = log_saver.read_logfiles(logfiles)  # Read logs
    for line in loglines:
        log = LogDatabase.parse_log(line)  # Parse logs
        if not log: continue
        if log["channel_code"] in DESIRED_CHANNEL_CODES:
            log_counter += 1
            fixed_log = LogDatabase.fix_log(log)  # Fix Logs
            log_db.insert_log(**fixed_log)  # Insert Logs
    print("database updated")


async def post_to_channel(channel_id: int, message: str):  # unused function for now
    """Posts a message to a specified Discord channel."""
    channel = bot.get_channel(channel_id)
    await channel.send(message)


# Base command for testing
logs = SlashCommand(
    name="logs",
    description="Commands involving logs"
)


# Subcommand for posting to a channel
@logs.subcommand(sub_cmd_name="read_logs",
                 sub_cmd_description="Posts logs to a channel")
@slash_option(
    name="start_date",
    description="start date of logs in cst. format: 2023-12-20T15:00:00",
    required=False,
    opt_type=OptionType.STRING)
@slash_option(
    name="end_date",
    description="start date of logs in cst. format: 2023-12-20T15:00:00",
    required=False,
    opt_type=OptionType.STRING)
@slash_option(
    name="authors",
    description="comma separated list of authors. eg. Haltise, Lyonette, Raspberry",
    required=False,
    opt_type=OptionType.STRING)
@slash_option(
    name="channel_codes",
    description="comma separated list of channel_codes eg. 000D, 000C",
    required=False,
    opt_type=OptionType.STRING)
@slash_option(
    name="channels",
    description="comma separated list of channels eg. Tell, Say, Party, Emote",
    required=False,
    opt_type=OptionType.STRING)
@slash_option(
    name="content",
    description="content to search for, eg. 'I just leveled up!'",
    required=False,
    opt_type=OptionType.STRING)
async def read_logs(ctx: SlashContext, start_date: str = "2000-12-20T15:00:00",
                    end_date: str = "2050-12-20T15:00:00", authors: str = None, channel_codes: str = None,
                    channels: str = None, content: str = None):
    log_db = LogDatabase(LogDatabase.db_name)
    start_datetime_cst = start_date
    end_datetime_cst = end_date

    filter_criteria = {}
    print(f"read_logs 1")
    if authors:
        filter_criteria['author'] = [author.strip() for author in authors.split(', ')]
    if content:
        filter_criteria['content'] = [content]
    if channel_codes:
        channel_codes = [code.strip().title() for code in channel_codes.split(',')]
    if channels:
        channels = [channel.strip().title() for channel in channels.split(',')]

    if channel_codes:
        filter_criteria["channel_code"] = [channel_code for channel_code in channel_codes if channel_code in
                                            DESIRED_CHANNEL_CODES]
    else:
        filter_criteria["channel_code"] = [channel for channel in DESIRED_CHANNEL_CODES]

    if channels:
        filter_criteria["channel"] = [channel for channel in channels if channel in DESIRED_CHANNELS]

    print(f"read_logs 2")
    if channels:
        print(filter_criteria["channel"])
    data = log_db.select_log(start_datetime_cst=start_datetime_cst,  # list of post dicts
                             end_datetime_cst=end_datetime_cst,
                             filter_criteria=filter_criteria)
    limit = 2001
    if data and len(data) > limit:
        data = data[0:limit]
    print(f"length of data: {len(data)}")

    print(f"read_logs 3")
    result_list = discord_spam_preparer(data)
    print(f"length of bundled result list: {len(result_list)}")
    bundled_list = post_bundler(result_list)
    print(f"length of bundled result list: {len(bundled_list)}")
    print(f"read_logs 4")

    await ctx.defer()
    for post in bundled_list:
        await ctx.send(post)
    if not len(bundled_list):
        await ctx.send("No posts found")
    print(f"read_logs done")


if __name__ == "__main__":
    update_database()
    bot = interactions.Client(token=config("BOT_TOKEN"))
    bot.start()
