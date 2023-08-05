from voluptuous import Any, Schema, ALLOW_EXTRA

from skywiserestclient import SkyWiseJSON
from skywiserestclient.validation import (datetime, datetime_to_str)
from skywiserestclient import SkyWiseException

from . import PlatformResource
from .style import Style
from .frame import ProductFrame
from .forecast import ProductForecast


class ProductException(SkyWiseException):
    pass


class Product(SkyWiseJSON, PlatformResource):
    """
    The Product class allows you to query platform products. More importantly,
    Product instances provide convenience methods for accessing other resources on
    Platform: frames, styles, datapoints, and map tiles.
    """

    _path = '/products'

    _deserialize = Schema({
        "id": unicode,
        "name": unicode,
        "description": unicode,
        "contentType": unicode,
        "source": unicode,
        "frames": Any(None, unicode),
        "forecasts": Any(None, unicode),
        "styles": unicode,
        "styleableLayers": [{
            "name": unicode,
            "type": unicode,
            "unit": Any(None, dict),
            "attributes": [dict]
        }],
        "startTime": datetime,
        "endTime": datetime,
        "aggregationPeriodInMinutes": int,
        "tags": dict
    }, extra=ALLOW_EXTRA)

    _serialize = Schema({
        "id": unicode,
        "name": unicode,
        "description": unicode,
        "contentType": unicode,
        "source": unicode,
        "frames": Any(None, unicode),
        "forecasts": Any(None, unicode),
        "styles": unicode,
        "styleableLayers": [{
            "name": unicode,
            "type": unicode,
            "unit": Any(None, dict),
            "attributes": [dict]
        }],
        "startTime": datetime_to_str,
        "endTime": datetime_to_str,
        "aggregationPeriodInMinutes": int,
        "tags": dict
    }, extra=ALLOW_EXTRA)

    _args = Schema({
        "contentType": str,
        "source": str,
        "aggregation": int,
        "start": datetime_to_str,
        "end": datetime_to_str
    }, extra=ALLOW_EXTRA)

    def __repr__(self):
        try:
            return '<Product %s>' % (self.name,)
        except:
            return super(Product, self).__repr__()

    @classmethod
    def find(cls, id_=None, aggregation=None, **kwargs):
        if aggregation is None:
            return super(Product, cls).find(id_=id_, **kwargs)

        if aggregation == 'day':
            aggregation = 1440
        elif aggregation == 'hour':
            aggregation = 60
        elif aggregation == 'minute':
            aggregation = 1

        return super(Product, cls).find(id_=id_, aggregation=aggregation, **kwargs)

    def has_forecast(self):
        return self._data['forecasts'] is not None

    def _styles(self):
        styles = Style.find(self.id)
        for style in styles:
            style.product = self
        return styles

    def _forecasts(self, **kwargs):
        forecasts = ProductForecast.find(self.id, **kwargs)
        for forecast in forecasts:
            forecast.product = self
        return forecasts

    def _frames(self, start=None, end=None, limit=None, reruns=None, **kwargs):
        if self._data['frames']:
            frames = ProductFrame.find(self.id, start=start, end=end, limit=limit, reruns=reruns, **kwargs)
        else:
            forecasts = self.forecasts()
            if not forecasts:
                return forecasts
            forecast = forecasts.pop()
            frames = forecast.frames(start=start, end=end, limit=limit, reruns=reruns, **kwargs)
        for frame in frames:
            frame.product = self
        return frames

    def __getattr__(self, item):
        if item == 'styles':
            return self._styles
        elif item == 'forecasts':
            return self._forecasts
        elif item == 'frames':
            return self._frames
        else:
            return super(Product, self).__getattr__(item)
