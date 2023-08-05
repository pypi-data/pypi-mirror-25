from declaration import fields, models


class Account(models.DeclarativeBase):
    pass


class Message(models.DeclarativeBase):
    conversation_id = fields.UUIDField()
    platform = fields.StringField()
    sender = fields.StringField()
    receiver = fields.StringField()
    timestamp = fields.DateTimeField()
    identifier = fields.StringField()
    content = fields.StringField()
    raw = fields.StringField()
