from peewee import *
from os import getenv
from datetime import datetime

db = SqliteDatabase(None)


def init_db(*args):
    db.init(*args)
    db.connect()
    db.create_tables([VoiceActivityLogs])
    return db


class VoiceActivityLogs(Model):
    member_id = CharField()
    channel_id = CharField()
    joined_at = DateTimeField()
    left_at = DateTimeField(null=True)
    orphan = BooleanField(default=False)

    class Meta:
        database = db

    def start_log(member_id, channel_id):
        # create VoiceActivityLogs database row with an empty left_at
        with db.atomic():
            row = VoiceActivityLogs.create(
                member_id=member_id,
                channel_id=channel_id,
                joined_at=datetime.now())
            row.save()

    def end_log(member_id, channel_id):
        # update row and set left_at field
        return (__class__
                .update(left_at=datetime.now())
                .where(__class__.member_id == member_id)
                .order_by(__class__.joined_at.desc())
                .limit(1)
                .execute())

    def end_orphan_logs(member_id):
        # attempt to find orphan log and end it
        return (__class__
                .update(left_at=datetime.now(), orphan=True)
                .where(__class__.member_id == member_id,
                       __class__.left_at == None)
                .execute())
