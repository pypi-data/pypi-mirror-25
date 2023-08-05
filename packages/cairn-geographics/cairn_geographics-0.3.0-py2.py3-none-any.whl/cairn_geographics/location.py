from cairn_geographics.gis_object import CairnGisObject

class Location(CairnGisObject):
    lat = None
    lon = None
    address = None

    def __init__(self, *args):
        super(Location, self).__init__()
        if len(args) == 2:
            self.lat = args[0]
            self.lon = args[1]
        elif len(args) == 1:
            self.address = args[0]

    def to_string(self):
        params = ', '.join('{name}={value}'.format(name=k, value=getattr(self, k))
                           for k in ['lat', 'lon', 'address']
                           if getattr(self, k, None) is not None)
        return "Location(%s)" % (params,)

    def region(self, region_type):
        return self.from_sexpr(["containing_region", self, region_type], result_type='Region')

    def driving_distance(self, end_location):
        return self.from_sexpr(["driving_distance", self, end_location], result_type='Measure')

    def driving_time(self, end_location):
        return self.from_sexpr(["driving_time", self, end_location], result_type='Measure')

    def component_sexpr(self):
        if self.address:
            if self.lat and self.lon:
                return ("location", self.lat, self.lon, self.address)
            else:
                return ("geocode", self.address)
        else:
            return ("location", self.lat, self.lon)

    @classmethod
    def from_dict(cls, data):
        assert data['type'] == 'Location'
        location = cls(data['lat'], data['lon'])
        if data.get('address'):
            location.address = data['address']
        location.evaluated = True
        return location
