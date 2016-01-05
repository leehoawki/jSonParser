import unittest
import jSonParser


class jSonParser_Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load(self):
        callback = str
        assert_iteself(jSonParser.load, callback, ('["foo", {"bar":["baz", null, 1.0, 2]}]'))
        assert_iteself(jSonParser.load, callback, '["\\"foo\\bar"]')

    def test_parse_object(self):
        callback = lambda x: str(x[0])
        assert_iteself(jSonParser.parse_obj, callback, '{"1":true}')
        assert_iteself(jSonParser.parse_obj, callback, '{"1":true, "wa":[1,2,3,4]}')
        assert_iteself(jSonParser.parse_obj, callback, '{"name":"test","age":"18"}')
        assert_iteself(jSonParser.parse_obj, callback, '{"people":null}')

    def test_parse_array(self):
        callback = lambda x: str(x[0])
        assert_iteself(jSonParser.parse_array, callback, '[1,\"w]a\"]haha')
        assert_iteself(jSonParser.parse_array, callback, "[1, true]")
        assert_iteself(jSonParser.parse_array, callback, "[1, true  ]")


def assert_iteself(fn, callback, input):
    r1 = callback(fn(input))
    r2 = callback(fn(r1))
    assert r1 == r2


if __name__ == '__main__':
    unittest.main()
