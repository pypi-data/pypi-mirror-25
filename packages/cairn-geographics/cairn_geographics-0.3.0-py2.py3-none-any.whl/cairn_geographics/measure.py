from cairn_geographics.gis_object import CairnGisObject

class Measure(CairnGisObject):
    value = None
    unit = None

    def __init__(self, *args):
        super(Measure, self).__init__()
        if args:
            self.value = args[0]
            self.unit = args[1]

    def __div__(self, other):
        # For Python 2 compatibility
        return self.__truediv__(other)

    def __truediv__(self, other):
        return self.from_sexpr(["divide", self, other], result_type='Measure')

    def __add__(self, other):
        return self.from_sexpr(["add", self, other], result_type='Measure')

    def __sub__(self, other):
        return self.from_sexpr(["subtract", self, other], result_type='Measure')

    def __mul__(self, other):
        return self.from_sexpr(["multiply", self, other], result_type='Measure')

    def to_string(self):
        return "Measure(value={value}, unit={unit})".format(
            value=self.value,
            unit=repr(self.unit),
        )

    def component_sexpr(self):
        return ("measure", self.value, self.unit)

    @classmethod
    def from_dict(cls, data):
        assert data['type'] == 'Measure'
        measure = cls(data['value'], data['unit'])
        measure.evaluated = True
        return measure
