from voluptuous import Schema

from skywiserestclient import SkyWiseJSON
from . import PlatformResource

_schema = Schema({
    "id": unicode,
    "name": unicode,
    "description": unicode,
    "css": unicode,
    "isDefault": bool,
    "product": unicode
})


class Style(SkyWiseJSON, PlatformResource):

    _path = "/products/{product_id}/styles"

    _deserialize = _schema
    _serialize = _schema

    @classmethod
    def find(cls, product_id, **kwargs):
        return super(Style, cls).find(product_id=product_id, **kwargs)
