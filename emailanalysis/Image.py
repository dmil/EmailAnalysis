from peewee import *

from emailanalysis.utils import logger
from emailanalysis.utils import get_text_from_image_url

from emailanalysis.Email import Email

from blessings import Terminal
t = Terminal()


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

    def ocr(self):
        logger.info(f"saving text for {self.id} from {self.url}")
        try:
            self.text = get_text_from_image_url(self.url)
            if self.text:
                logger.debug(f"Found Text:\n{self.text}")
        except:
            logger.warn(t.red('ERROR'))
            self.text = 'ERROR'
        self.save()


    def __str__(self):
        return "Url: %s\nText:" % (self.url, self.text)
