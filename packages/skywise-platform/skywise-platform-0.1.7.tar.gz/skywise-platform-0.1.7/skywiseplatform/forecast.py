from voluptuous import Any, Schema

from skywiserestclient import SkyWiseJSON

from skywiserestclient.validation import datetime, datetime_to_str
from skywiseplatform import PlatformResource, ForecastFrame


_forecast_deserialize_schema = Schema({
    "id": unicode,
    "initTime": datetime,
    "creationTime": datetime,
    "expirationTime": datetime,
    "frames": unicode
})

_forecast_serialize_schema = Schema({
    "id": unicode,
    "initTime": datetime_to_str,
    "creationTime": datetime_to_str,
    "expirationTime": datetime_to_str,
    "frames": unicode
})


class _Forecast(SkyWiseJSON, PlatformResource):

    def _frames(self, start=None, end=None, **kwargs):
        frames = ForecastFrame.find(self.id, start=start, end=end, **kwargs)
        for frame in frames:
            frame.forecast = self
            frame.product = self.product
        return frames

    def __getattr__(self, item):
        if item == 'frames':
            return self._frames
        return super(_Forecast, self).__getattr__(item)

    def __repr__(self):
        try:
            return '<Forecast %s>' % (self.initTime,)
        except:
            return super(_Forecast, self).__repr__()


class Forecast(_Forecast):

    _path = '/forecasts'

    _deserialize = _forecast_deserialize_schema
    _serialize = _forecast_serialize_schema


class ProductForecast(_Forecast):

    _path = "/products/{product_id}/forecasts"

    _deserialize = _forecast_deserialize_schema
    _serialize = _forecast_serialize_schema

    _args = Schema({
        "start": datetime_to_str,
        "end": datetime_to_str,
        "limit": int,
        "sort": Any("asc", "desc")
    })

    @classmethod
    def find(cls, product_id, **kwargs):
        forecasts = super(ProductForecast, cls).find(product_id=product_id, **kwargs)
        forecasts.sort(key=lambda f: f.initTime)
        return forecasts
