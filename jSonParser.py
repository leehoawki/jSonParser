class MyObject(object):
    def __init__(self):
        self.__str__ = self.__repr__


class JObject(MyObject):
    def __init__(self, o):
        super(JObject, self).__init__()
        self.o = o

    def __repr__(self):
        ol = map(lambda x: str(x[0]) + ":" + str(x[1]), self.o)
        return "{" + ",".join(ol) + "}"

    def __getitem__(self, item):
        for k, v in self.o:
            if k.a == item:
                return v
        raise ParseException("No such key in object : %s" % self)

    def __setitem__(self, key, value):
        count = 0
        for k, v in self.o:
            if k.a == key:
                if not isinstance(value, MyObject):
                    raise ParseException("Illegal type object: %s" % value)
                self.o[count] = (k, value)
                return
            count += 1
        self.o.append((JString(key), value))


class JArray(MyObject):
    def __init__(self, l):
        super(JArray, self).__init__()
        self.l = l

    def __repr__(self):
        return "[" + ",".join(map(str, self.l)) + "]"

    def __getitem__(self, item):
        return self.l[item]

    def __setitem__(self, key, value):
        self.l[key] = value

    def append(self, item):
        self.l.append(item)

    def remove(self, item):
        self.l.remove(item)


class JString(MyObject):
    def __init__(self, a):
        super(JString, self).__init__()
        self.a = a

    def __repr__(self):
        return '"' + self.a + '"'


class JNumber(MyObject):
    def __init__(self, n):
        super(JNumber, self).__init__()
        self.n = n

    def __repr__(self):
        return str(self.n)


class JBool(MyObject):
    def __init__(self, b):
        super(JBool, self).__init__()
        self.b = b

    def __repr__(self):
        if self.b:
            return "true"
        return "false"


class JNull(MyObject):
    def __init__(self):
        super(JNull, self).__init__()

    def __repr__(self):
        return "null"


class ParseException(Exception):
    pass


def load(s):
    s = trim(s)
    if len(s) == 0:
        raise ParseException("Empty string.")

    if s[0] == "{":
        o = parse_obj(s)
        return o[0]
    elif s[0] == "[":
        a = parse_array(s)
        return a[0]
    else:
        raise ParseException("Parse error: %s" % s)


def trim(s):
    index = 0
    whites = " \r\n"
    while index < len(s) and s[index] in whites:
        index += 1
    return s[index:]


def parse_obj(s):
    s = trim(s[1:])
    if s[0] == "}":
        return JObject([]), s[1:]
    l = []
    while True:
        if s[0] != '"':
            raise ParseException('Expecting a "')
        key, s = parse_string(s)
        s = trim(s)
        if s[0] != ':':
            raise ParseException('Expecting a :')
        s = trim(s[1:])
        val, s = parse_value(s)
        s = trim(s)
        l.append((key, val))
        if s[0] == ',':
            s = trim(s[1:])
        elif s[0] == '}':
            return JObject(l), s[1:]
        else:
            raise ParseException('Expecting a , or }')


def parse_array(s):
    s = trim(s[1:])
    if s[0] == "]":
        return JArray([]), s[1:]
    a = []
    while True:
        val, s = parse_value(s)
        a.append(val)
        s = trim(s)
        if s[0] == ',':
            s = trim(s[1:])
        elif s[0] == ']':
            return JArray(a), s[1:]
        else:
            raise ParseException('Expecting a , or ]')


def parse_string(s):
    index = 1
    escape = False
    while index < len(s):
        if escape:
            escape = False
        elif s[index] == '"':
            break
        elif s[index] == '\\':
            escape = True
        index += 1
    if index >= len(s) or s[index] != '"':
        raise ParseException('Expecting a "')
    return JString(s[1:index]), s[index + 1:]


def parse_null(s):
    if s.startswith("null"):
        return JNull(), s[4:]
    else:
        raise ParseException("Failed to parse: %s" % s)


def parse_true(s):
    if s.startswith("true"):
        return JBool(True), s[4:]
    else:
        raise ParseException("Failed to parse: %s" % s)


def parse_false(s):
    if s.startswith("false"):
        return JBool(False), s[5:]
    else:
        raise ParseException("Failed to parse: %s" % s)


def parse_number(s):
    index = 0
    ns = "1234567890-+."
    while index < len(s) and s[index] in ns:
        index += 1
    try:
        return JNumber(float(s[:index])), s[index:]
    except Exception:
        raise ParseException("Failed to parse: %s" % s)


def parse_value(s):
    if s[0] == "n":
        return parse_null(s)
    if s[0] == "t":
        return parse_true(s)
    if s[0] == "f":
        return parse_false(s)
    if s[0] == '"':
        return parse_string(s)
    if s[0] == "{":
        return parse_obj(s)
    if s[0] == "[":
        return parse_array(s)
    else:
        return parse_number(s)
