from __init__ import get_client, run_client
from database import VoiceActivityLogs

client = get_client()


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
        print(f"{member.name} switched channels")


run_client()
