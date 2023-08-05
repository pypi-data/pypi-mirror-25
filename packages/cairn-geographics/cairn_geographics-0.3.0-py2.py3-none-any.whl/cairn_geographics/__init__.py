from cairn_geographics.type_factory import Location, Region, Measure, type_lookup
from cairn_geographics.connection import Connection
from cairn_geographics.region import State, ZipCode

Measure._type_lookup = type_lookup
Region._type_lookup = type_lookup
Location._type_lookup = type_lookup
