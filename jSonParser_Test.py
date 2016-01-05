import unittest
import jSonParser


class jSonParser_Test(unittest.TestCase):
    def test_load(self):
        callback = str
        assert_iteself(jSonParser.load, callback, ('["foo", {"bar":["baz", null, 1.0, 2]}]'))
        assert_iteself(jSonParser.load, callback, '["\\"foo\\bar"]')

        long_text = """{
            "programmers": [{
                "firstName": "Brett",
                "lastName": "McLaughlin",
                "email": "aaaa"
            }, {
                "firstName": "Jason",
                "lastName": "Hunter",
                "email": "bbbb"
            }, {
                "firstName": "Elliotte",
                "lastName": "Harold",
                "email": "cccc"
            }],
            "authors": [{
                "firstName": "Isaac",
                "lastName": "Asimov",
                "genre": "sciencefiction"
            }, {
                "firstName": "Tad",
                "lastName": "Williams",
                "genre": "fantasy"
            }, {
                "firstName": "Frank",
                "lastName": "Peretti",
                "genre": "christianfiction"
            }],
            "musicians": [{
                "firstName": "Eric",
                "lastName": "Clapton",
                "instrument": "guitar"
            }, {
                "firstName": "Sergei",
                "lastName": "Rachmaninoff",
                "instrument": "piano"
            }]
        }
        """
        assert_iteself(jSonParser.load, callback, long_text)

    def test_update(self):
        long_text = """{
            "programmers": [{
                "test": "test"
            }],
            "authors": [{
                "firstName": "Isaac",
                "lastName": "Asimov"
            }, {
                "firstName": "Tad",
                "lastName": "Williams"
            }]
        }
        """
        r = jSonParser.load(long_text)
        r["authors"][0]["firstName"] = jSonParser.JString("Test_F")
        r["authors"][0]["midlleName"] = jSonParser.JString("Test_M")
        r["authors"].append(jSonParser.JNull())
        r["authors"].append(jSonParser.JBool(True))
        r["authors"].append(jSonParser.JString("xxx"))
        assert str(r["authors"][0]) == '{"firstName":"Test_F","lastName":"Asimov","midlleName":"Test_M"}'
        assert str(r["authors"][2]) == 'null'
        assert str(r["authors"][3]) == 'true'
        assert str(r["authors"][4]) == '"xxx"'

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
