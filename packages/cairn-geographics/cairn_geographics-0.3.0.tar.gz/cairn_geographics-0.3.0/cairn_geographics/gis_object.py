def arg_from_type(cairn_gis_type):
    patched_object = cairn_gis_type()
    patched_object.sexpr = lambda: ("arg",)
    return patched_object

def get_type(typename):
    __import__(typename)

class CairnGisObject(object):
    value_type = None
    evaluated = False
    _sexpr = None
    _type_lookup = {}

    def sexpr(self):
        return self._sexpr if self._sexpr else self.component_sexpr()

    def component_sexpr(self):
        raise NotImplementedError('CairnGisObject must be subclassed, not used directly.')

    def to_string(self):
        raise NotImplementedError('CairnGisObject must be subclassed, not used directly.')

    def compile(self):
        return self._compile_sexpr(self.sexpr())

    def __repr__(self):
        if self.evaluated:
            return self.to_string()
        else:
            return "<CairnGis Query: Result Type %s>" % (type(self).__name__,)

    def _compile_sexpr(self, sexpr):
        tail = [self._format_arg(arg) for arg in sexpr[1:]]
        return '(' + ' '.join([sexpr[0]] + tail) + ')'

    def _format_arg(self, arg):
        if isinstance(arg, str):
            return '"' + arg.replace('\\', '\\\\').replace('"', '\\"') + '"'
        elif isinstance(arg, tuple):
            return self._compile_sexpr(arg)
        else:
            return str(arg)

    def from_sexpr(self, args, result_type=None):
        sexpr = tuple(arg.sexpr() if isinstance(arg, CairnGisObject) else arg
                      for arg in args)
        constructor = self._type_lookup.get(result_type, CairnGisObject)
        new_object = constructor()
        new_object._sexpr = sexpr
        new_object.value_type = self.value_type
        return new_object
