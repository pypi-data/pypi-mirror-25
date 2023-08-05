
def build_opt(o_type, o_name, o_val):
    # yield a new opt for multi-value options(--volume, --env, etc.)
    if o_type == ValueOpt and isinstance(o_val, list):
        for val in o_val:
            yield o_type(o_name, val)
    elif o_type == MapOpt:
        for k,v in o_val.items():
            val = '%s=%s' % (k,v)
            yield MapOpt(o_name, val)
    else:
        yield o_type(o_name, o_val)

class DockerArg(object):
    def __init__(self, name, val):
        self.name = name
        self.value = val

    def is_null(self):
        if self.value:
            return False
        return True

    def __str__(self):
        return self.value

class DockerOpt(object):
    def __init__(self, opt, val):
        self.opt = opt
        self.value = val

    def is_null(self):
        if self.value:
            return False
        return True

    def __str__(self):
        return '%s %s' % (self.opt, self.value)

class BoolOpt(DockerOpt):
    def __init__(self, *args):
        DockerOpt.__init__(self, *args)

    def __str__(self):
        return self.opt

class ByteValueOpt(DockerOpt):
    """ Option with one or more user-defined values """
    def __init__(self, *args):
        DockerOpt.__init__(self, *args)

    @staticmethod
    def format_bytes(x):
        KB = 1024
        MB = KB*1024
        GB = MB*1024
        x = float(x)
        if x < 1024:
            return '%sb' % round(x)
        elif 1024 <= x < MB:
            return '%sk' % round(x/KB)
        elif KB <= x < GB:
            return '%sm' % round(x/MB)
        elif GB <= x:
            return '%sg' % round(x/GB)

    def __str__(self):
        try:
            return '%s %s' % (self.opt, self.format_bytes(self.value))
        except ValueError:
            raise TypeError('unsupported value type for option "%s": %s' % \
                    (self.opt, self.value))

class ValueOpt(DockerOpt):
    """ Option with one or more user-defined values """

    def __init__(self, *args):
        DockerOpt.__init__(self, *args)

    def __str__(self):
        try:
            return '%s %s' % (self.opt, self.value)
        except ValueError:
            raise TypeError('unsupported value type for option "%s": %s' % \
                    (self.opt, self.value))

class MapOpt(ValueOpt):
    """ Option with one or more user-defined mappings """
    def __init__(self, *args):
        ValueOpt.__init__(self, *args)
