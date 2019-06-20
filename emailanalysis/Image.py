from peewee import *

from emailanalysis.utils import logger
from emailanalysis.Email import Email

db = SqliteDatabase('emails.db')

class Image(Model):
    url = TextField(null=True, default=None)
    text = TextField(null=True, default=None)
    email = ForeignKeyField(Email, null=True, default=None)

    class Meta:
        database = db

    @classmethod
    def create(cls, **query):
        inst = cls(**query)
        inst.save(force_insert=True)
        inst._prepare_instance()
        logger.info("Created Image %s", inst.url)
        return inst

    def _prepare_instance(self):
        self._dirty.clear()
        self.prepared()

    def prepared(self):
        pass

    def __str__(self):
        return "Url: %s\nText:" % (self.url, self.text)
