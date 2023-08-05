from voluptuous import Any, Schema, Required

from skywiserestclient import SkyWiseJSON
from . import PlatformResource


class Datapoint(SkyWiseJSON, PlatformResource):

    _path = "/frames/{frame_id}/datapoint/{latitude}/{longitude}"

    _deserialize = Schema({
        "tile": unicode,
        "pixel": {
            "row": int,
            "column": int
        },
        Required("value"): Any(None, float),
        "unit": {
            "description": unicode,
            "label": unicode
        }
    })

    _serialize = Schema({
        "tile": unicode,
        "pixel": {
            "row": int,
            "column": int
        },
        Required("value"): Any(None, float),
        "unit": {
            "description": unicode,
            "label": unicode
        }
    })

    @classmethod
    def find(cls, frame, latitude, longitude, **kwargs):
        r = super(Datapoint, cls).find(frame_id=frame.id, latitude=latitude, longitude=longitude, **kwargs)
        r.frame = frame
        r.validTime = frame.validTime
        return r

    @classmethod
    def find_async(cls, frame, latitude, longitude, **kwargs):
        r = super(Datapoint, cls).find_async(frame_id=frame.id, latitude=latitude, longitude=longitude, **kwargs)
        r.tag(frame=frame, validTime=frame.validTime)
        return r
