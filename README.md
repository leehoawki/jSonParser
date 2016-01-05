# jSonParser
jSonParser is a Json Parser.

It allows you to load json format string,

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
        
        r = jSonParser.load(long_text)
        r["authors"][0]["firstName"] = jSonParser.JString("Test_F")
        r["authors"][0]["midlleName"] = jSonParser.JString("Test_M")
        print r["authors"][0]
        r["authors"].append(JBool(True))
        print r

and dump the json objects/arrays into string after modifying.