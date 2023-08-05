from voluptuous import Any, Schema

from skywiserestclient import SkyWiseJSON
from skywiserestclient.validation import datetime, datetime_to_str

from skywiseplatform import PlatformResource, GoogleMapsTile, BingMapsTile, Datapoint


class _Frame(SkyWiseJSON, PlatformResource):

    _args = Schema({
        "start": datetime_to_str,
        "end": datetime_to_str,
        "limit": int,
        "sort": Any("asc", "desc"),
        "reruns": bool
    })

    _deserialize = Schema({
        "id": unicode,
        "validTime": datetime,
        "runTime": datetime,
        "creationTime": datetime,
        "zoomLevels": {
            "minimum": int,
            "native": int,
            "maximum": int
        },
        "mediaTypes": [unicode],
        "tileSize": int,
        "forecast": Any(None, unicode)
    })

    _serialize = Schema({
        "id": unicode,
        "validTime": datetime_to_str,
        "runTime": datetime_to_str,
        "creationTime": datetime_to_str,
        "zoomLevels": {
            "minimum": int,
            "native": int,
            "maximum": int
        },
        "mediaTypes": [unicode],
        "tileSize": int,
        "forecast": Any(None, unicode)
    })

    def _tile(self, x=None, y=None, z=None, quadkey=None, **kwargs):
        if x is not None and y is not None and z is not None:
            tile = GoogleMapsTile.find(self.id, x, y, z, **kwargs)
        elif quadkey is not None:
            tile = BingMapsTile.find(self.id, quadkey, **kwargs)
        else:
            raise Exception("You failed to provide either x/y/z coords or a quadkey.")
        tile.frame = self
        return tile

    def _tile_async(self, x=None, y=None, z=None, quadkey=None, **kwargs):
        if x is not None and y is not None and z is not None:
            tile = GoogleMapsTile.find_async(self.id, x, y, z, **kwargs)
        elif quadkey is not None:
            tile = BingMapsTile.find_async(self.id, quadkey, **kwargs)
        else:
            raise Exception("You failed to provide either x/y/z coords or a quadkey.")
        tile.tag(frame=self)
        return tile

    def _datapoint(self, lat, lon):
        datapoint = Datapoint.find(self, lat, lon)
        datapoint.frame = self
        return datapoint

    def _datapoint_async(self, lat, lon):
        datapoint = Datapoint.find_async(self, lat, lon)
        datapoint.tag(frame=self)
        return datapoint

    def __getattr__(self, item):
        if item == 'tile':
            return self._tile
        elif item == 'tile_async':
            return self._tile_async
        elif item == 'datapoint':
            return self._datapoint
        elif item == 'datapoint_async':
            return self._datapoint_async
        else:
            return super(_Frame, self).__getattr__(item)


class SingleFrame(_Frame):

    _path = "/frames"


class ProductFrame(_Frame):
    """Requests product frames.
    """

    _path = "/products/{product_id}/frames"

    @classmethod
    def find(cls, product_id, start=None, end=None, limit=None, sort=None, reruns=None, **kwargs):
        """Requests frames for a product.

        Example:
            .. code-block:: python

               import skywise

        Args:
            product_id (str): the product you're requesting frames for.
            start (datetime): The start date for your frame date range.
            end (datetime): The end date for your frame date range.
            limit (int): The maximum number of frames you are requesting.
            reruns (bool): Whether or not you would like multiple frames for particular time.

        Returns:
            list of ProductFrame: A list of frames for the product.

        """
        return super(ProductFrame, cls).find(product_id=product_id, start=start, end=end,
                                             limit=limit, sort=sort, reruns=reruns, **kwargs)


class ForecastFrame(_Frame):
    """Requests Forecast Frames.

    Attributes:
        id (str): the frame's id.
        validTime (datetime): when the frame is valid
        runTime (datetime): when the frame was ran
        zoomLevels (dict): minimum, native, and maximum zoom level specifications
        mediaTypes (str): list of supported types: image/jpeg, image/png, or image/tiff
        tileSize (int): tile size
        forecast (str): url to the frame's forecast
    """
    _path = "/forecasts/{forecast_id}/frames"

    @classmethod
    def find(cls, forecast_id, start=None, end=None, limit=None, sort=None, reruns=None, **kwargs):
        """Requests frames for a product.

        Example:
            .. code-block:: python

                forecast_id = Product.find('weatherops-24hr-precipitation-forecast').id

                # Retrieve latest frames
                frames = ForecastFrame.find(product_id)

                # Retrieve frames for next few days
                start = arrow.get().datetime
                end = arrow.get().replace(days=+5).datetime
                frames = ForecastFrame.find(forecast_id, start=start, end=end, limit=3, sort="desc")

        Args:
            forecast_id (str): the forecast you're requesting frames for.
            start (datetime): The start date for your frame date range.
            end (datetime): The end date for your frame date range.
            limit (int): The maximum number of frames you are requesting.
            reruns (bool): Whether or not you would like multiple frames for particular time.

        Returns:
            list of ForecastFrame: A list of frames for the product.

        """
        return super(ForecastFrame, cls).find(forecast_id=forecast_id, start=start, end=end,
                                              limit=limit, sort=sort, reruns=reruns, **kwargs)
