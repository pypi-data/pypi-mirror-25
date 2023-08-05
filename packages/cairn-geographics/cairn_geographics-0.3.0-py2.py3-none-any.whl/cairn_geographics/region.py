from cairn_geographics.gis_object import CairnGisObject

class Region(CairnGisObject):
    region_type = None
    key = None
    name = None

    def __init__(self, *args):
        super(Region, self).__init__()

        if args:
            self.region_type = args[0]
            self.key = args[1]

    def to_string(self):
        return "Region(region_type={region_type}, key={key}, name={name})".format(
            region_type=self.region_type,
            key=self.key,
            name=self.name,
        )

    def centroid(self):
        return self.from_sexpr(["centroid", self], result_type='Location')

    def area(self):
        return self.from_sexpr(["area", self], result_type='Measure')

    def demographics(self, demographics_type):
        return self.from_sexpr(["demographics", self, demographics_type], result_type='Measure')

    def component_sexpr(self):
        return ("region", self.region_type, self.key)

    @classmethod
    def from_dict(cls, data):
        assert data['type'] == 'Region'
        region = cls(data['region_type'], data['key'])
        region.name = data.get('name')
        region.evaluated = True
        return region

class State(Region):
    def __init__(self, usps_code):
        super(State, self).__init__('us_state', usps_code)

class ZipCode(Region):
    def __init__(self, zip5):
        super(ZipCode, self).__init__('zip_code', zip5)