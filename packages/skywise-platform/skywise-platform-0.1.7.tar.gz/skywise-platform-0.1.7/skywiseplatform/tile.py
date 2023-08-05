import math

from skywiserestclient import SkyWiseImage
from . import PlatformResource, Style


_MinLatitude = -85.05112878
_MaxLatitude = 85.05112878
_MinLongitude = -180.0
_MaxLongitude = 180.0


class MapTile(SkyWiseImage, PlatformResource):

    _style_id = None

    @classmethod
    def get_style(cls):
        return cls._style_id

    @classmethod
    def set_style(cls, style_id):
        cls._style_id = style_id

    @classmethod
    def map_size(cls, zoom):
        """
        Determines the map width and height (in pixels) at a specified level
        of detail (1 to 23).

        Returns map width (=height) in pixels.
        """
        return 256 << int(zoom)

    @classmethod
    def clip(cls, n, minValue, maxValue):
        """ Clips a number to the specified minimum and maximum values. """
        return min(max(n, minValue), maxValue)

    @classmethod
    def lat_lon_to_pixel_xy(cls, latitude, longitude, zoomlevel):
        """
        Converts a point from latitude/longitude WGS-84 coordinates (in degrees)
        into pixel XY coordinates at a specified level of detail.
        """
        latitude = cls.clip(latitude, _MinLatitude, _MaxLatitude)
        longitude = cls.clip(longitude, _MinLongitude, _MaxLongitude)

        x = (longitude + 180) / 360
        sinLatitude = math.sin(math.radians(latitude))
        y = 0.5 - math.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * math.pi)

        map_size = cls.map_size(zoomlevel)
        pixel_x = int(cls.clip(x * map_size + 0.5, 0, map_size - 1))
        pixel_y = int(cls.clip(y * map_size + 0.5, 0, map_size - 1))

        return pixel_x, pixel_y

    @classmethod
    def pixel_xy_to_tile_xy(cls, pixel_x, pixel_y):
        """
        Converts pixel XY coordinates into tile XY coordinates of the tile containing
        the specified pixel.
        """
        tile_x = int(pixel_x) / 256
        tile_y = int(pixel_y) / 256

        return tile_x, tile_y

    @classmethod
    def tile_range(cls, lat_lon_bounding_box, z, padding=None):
        n, e = lat_lon_bounding_box[0]
        s, w = lat_lon_bounding_box[1]
        pixel_xmax, pixel_ymin = cls.lat_lon_to_pixel_xy(n, e, z)
        pixel_xmin, pixel_ymax = cls.lat_lon_to_pixel_xy(s, w, z)

        if padding is not None:
            # Find how close to each edge of a tile we are, and if we are less than our padding,
            # grab an additional tile for that edge.
            if pixel_ymin % 256 < padding:
                pixel_ymin -= padding
            if pixel_xmax % 256 < padding:
                pixel_xmax += padding
            if pixel_xmin % 256 < padding:
                pixel_xmin -= padding
            if pixel_ymax % 256 < padding:
                pixel_ymax += padding

        xmax, ymin = cls.pixel_xy_to_tile_xy(pixel_xmax, pixel_ymin)
        xmin, ymax = cls.pixel_xy_to_tile_xy(pixel_xmin, pixel_ymax)

        return [(x, y) for x in xrange(xmin, xmax + 1) for y in xrange(ymin, ymax + 1)]

    @classmethod
    def tile_to_quadkey(cls, x=0, y=0, z=0):
        """ Convert the Google Maps tile coordinate to a Bing Maps quadkey. """
        quadkey = ''
        for i in xrange(z, 0, -1):
            digit = 0
            mask = 1 << (i - 1)

            if (x & mask) != 0:
                digit += 1
            if (y & mask) != 0:
                digit += 2
            quadkey += str(digit)
        return quadkey

    @classmethod
    def find(cls, style=None, media_type=None, **kwargs):
        _media_type = media_type or cls._media_type
        _style_id = cls._style_id
        if style is not None and type(style) is Style:
            _style_id = style.id
        elif style is not None:
            _style_id = style

        headers = {}
        if _style_id:
            headers['Accept'] = "%s; style=%s; version=1" % (_media_type, _style_id)
        else:
            headers['Accept'] = "%s; version=1" % _media_type
        return super(MapTile, cls).find(headers=headers, **kwargs)

    @classmethod
    def find_async(cls, style=None, media_type=None, **kwargs):
        _media_type = media_type or cls._media_type
        _style_id = cls._style_id
        if style is not None and type(style) is Style:
            _style_id = style.id
        elif style is not None:
            _style_id = style

        headers = {}
        if _style_id:
            headers['Accept'] = "%s; style=%s; version=1" % (_media_type, _style_id)
        else:
            headers['Accept'] = "%s; version=1" % _media_type
        return super(MapTile, cls).find_async(headers=headers, **kwargs)

    @classmethod
    def get_headers(cls):
        headers = super(MapTile, cls).get_headers()
        if cls._style_id:
            headers['Accept'] = "%s; style=%s; version=1" % (cls._media_type, cls._style_id)
        return headers

class GoogleMapsTile(MapTile):

    _path = "/frames/{frame_id}/tile/{z}/{x}/{y}"
    _media_type = 'image/tiff'

    @classmethod
    def find(cls, frame_id, x, y, z, **kwargs):
        tile = super(GoogleMapsTile, cls).find(frame_id=frame_id, x=x, y=y, z=z, **kwargs)
        tile.x = x
        tile.y = y
        tile.z = z
        return tile

    @classmethod
    def find_async(cls, frame_id, x, y, z, **kwargs):
        tile_request = super(GoogleMapsTile, cls).find_async(frame_id=frame_id, x=x, y=y, z=z, **kwargs)
        tile_request.tag(x=x, y=y, z=z)
        return tile_request

    @classmethod
    def tileset(cls, frame_id, lat_lon_bounding_box, z, padding=None):
        requests = cls.tileset_async(frame_id, lat_lon_bounding_box, z, padding=padding)
        return cls.map(requests)

    @classmethod
    def tileset_async(cls, frame_id, lat_lon_bounding_box, z, padding=None):
        tile_range = cls.tile_range(lat_lon_bounding_box, z, padding=padding)
        return [cls.find_async(frame_id, tile[0], tile[1], z) for tile in tile_range]


class BingMapsTile(MapTile):

    _path = "/frames/{frame_id}/tile/{quadkey}"
    _media_type = 'image/tiff'

    @classmethod
    def find(cls, frame_id, quadkey, **kwargs):
        tile = super(BingMapsTile, cls).find(frame_id=frame_id, quadkey=quadkey, **kwargs)
        tile.quadkey = quadkey
        return tile

    @classmethod
    def find_async(cls, frame_id, quadkey, **kwargs):
        tile_request = super(BingMapsTile, cls).find_async(frame_id=frame_id, quadkey=quadkey, **kwargs)
        tile_request.tag(quadkey=quadkey)
        return tile_request
