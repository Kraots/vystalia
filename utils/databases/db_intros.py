from . import database1, GetDoc

from umongo.fields import *
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance as Instance
from umongo.frameworks.motor_asyncio import MotorAsyncIODocument as Document

instance = Instance(database1)


@instance.register
class Intro(Document, GetDoc):
    id = IntField(attribute='_id', required=True)

    name = StrField(required=True)
    age = IntField(required=True)
    pronouns = StrField(required=True)
    gender = StrField(required=True)
    location = StrField(required=True)
    dms = StrField(required=True)

    sexuality = StrField(required=True)
    likes = StrField(required=True)
    dislikes = StrField(required=True)

    message_id = IntField(required=True)

    class Meta:
        collection_name = 'Intros'
