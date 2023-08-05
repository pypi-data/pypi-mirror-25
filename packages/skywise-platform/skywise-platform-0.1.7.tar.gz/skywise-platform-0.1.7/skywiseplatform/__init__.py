import os

from skywiserestclient import SkyWiseResource


class PlatformResource(SkyWiseResource):
    pass

_site = os.getenv('SKYWISE_PLATFORM_SITE', 'http://platform.api.wdtinc.com')
_user = os.getenv('SKYWISE_PLATFORM_APP_ID', '')
_password = os.getenv('SKYWISE_PLATFORM_APP_KEY', '')

PlatformResource.set_site(_site)
PlatformResource.set_user(_user)
PlatformResource.set_password(_password)


def map_async(skywise_requests, raise_on_error=True):
    return PlatformResource.map(skywise_requests, raise_on_error=raise_on_error)


from .style import Style
from .tile import BingMapsTile, GoogleMapsTile
from .datapoint import Datapoint
from .frame import ProductFrame, ForecastFrame
from .product import Product
from .forecast import Forecast
