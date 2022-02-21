import os
import discord
from logs_db import get_db as get_logs_db, VoiceActivityLogs
from dotenv import load_dotenv

client = discord.Client()
load_dotenv()

logs_db = get_logs_db()
logs_db.connect()
logs_db.create_tables([VoiceActivityLogs])


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_voice_state_update(member, before, after):
    # user joined channel
    if before.channel is None and after.channel is not None:
        VoiceActivityLogs.end_orphan_logs(member.id)
        VoiceActivityLogs.start_log(member.id, after.channel.id)  # new row
        print(f"{member.name} joined")

    # user left channel
    elif before.channel is not None and after.channel is None:
        VoiceActivityLogs.end_log(member.id, before.channel.id)  # set left_at
        print(f"{member.name} left")

    # user switched channel
    elif before.channel is not None and after.channel is not None:
        VoiceActivityLogs.end_log(member.id, before.channel.id)  # end
        VoiceActivityLogs.start_log(member.id, after.channel.id)  # start
        print(f"{member.name} switched rooms")


client.run(os.getenv('DISCORD_TOKEN'))
