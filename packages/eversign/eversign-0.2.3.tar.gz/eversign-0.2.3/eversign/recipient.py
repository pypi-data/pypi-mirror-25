from schematics.types import StringType, EmailType
from schematics.models import Model

from .utils import BaseObject, BoolIntType


class Recipient(BaseObject):

    def __init__(self, name=None, email=None, **kwargs):
        kwargs['name'] = name
        kwargs['email'] = email

        kwargs = self.clear_kwargs(kwargs)
        self.__dict__['_model'] = RecipientModel(kwargs, strict=False)
        self._model.validate()


class RecipientModel(Model):

    name = StringType(required=True)
    email = EmailType(required=True)
    role = StringType()
    message = StringType()
    required = BoolIntType()

    class Options:
        serialize_when_none = False
