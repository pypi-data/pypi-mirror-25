import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as asserts

@t.test(0)
def key1(test):
    def testMethod():
        import sys
        sys.argv = ["caesar.py", "1"]
        stdinArgs = ["a"]
        output = lib.outputOf(_fileName, stdinArgs)
        line = lib.getLine(output, 0)
        return asserts.contains(line, "b")

    test.test = testMethod
    test.description = lambda : "encrypts a as b using 1 as key"

@t.test(10)
def key23(test):
    def testMethod():
        import sys
        sys.argv = ["caesar.py", "23"]
        stdinArgs = ["barfoo"]
        output = lib.outputOf(_fileName, stdinArgs)
        line = lib.getLine(output, 0)
        return asserts.contains(line, "yxocll")

    test.test = testMethod
    test.description = lambda : "encrypts barfoo as yxocll using 23 as key"

@t.test(20)
def key3(test):
    def testMethod():
        import sys
        sys.argv = ["caesar.py", "3"]
        stdinArgs = ["BARFOO"]
        output = lib.outputOf(_fileName, stdinArgs)
        line = lib.getLine(output, 0)
        return asserts.contains(line, "EDUIRR")

    test.test = testMethod
    test.description = lambda : "encrypts BARFOO as EDUIRR using 3 as key"

@t.test(30)
def key4(test):
    def testMethod():
        import sys
        sys.argv = ["caesar.py", "4"]
        stdinArgs = ["BaRFoo"]
        output = lib.outputOf(_fileName, stdinArgs)
        line = lib.getLine(output, 0)
        return asserts.contains(line, "FeVJss")

    test.test = testMethod
    test.description = lambda : "encrypts BaRFoo as FeVJss using 4 as key"

@t.test(40)
def key65(test):
    def testMethod():
        import sys
        sys.argv = ["caesar.py", "65"]
        stdinArgs = ["barfoo"]
        output = lib.outputOf(_fileName, stdinArgs)
        line = lib.getLine(output, 0)
        return asserts.contains(line, "onesbb")

    test.test = testMethod
    test.description = lambda : "encrypts barfoo as onesbb using 65 as key"

@t.test(50)
def invalidInput(test):
    def testMethod():
        import sys
        sys.argv = ["caesar.py"]
        stdinArgs = ["foo"]
        output = lib.outputOf(_fileName, stdinArgs)
        line = lib.getLine(output, 0)
        return asserts.contains(line, "usage: python caesar.py key")

    test.test = testMethod
    test.description = lambda : "handles lack of argv[1]"
