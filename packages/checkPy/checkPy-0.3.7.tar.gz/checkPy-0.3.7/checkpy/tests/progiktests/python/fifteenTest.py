import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as asserts
import re

@t.test(0)
def shows3x3(test):
    def testMethod():
        import sys
        sys.argv = ["fifteen.py", "3"]
        stdinArgs = ["-1"]
        output = lib.outputOf(_fileName, stdinArgs)
        regex = re.compile(".*"
	      "(08 07 06)[ ]*(\n)"
	      "(05 04 03)[ ]*(\n)"
	      "(02 01 __)[ ]*(\n)"
	      ".*", re.MULTILINE)
        return asserts.match(output, regex)

    test.test = testMethod
    test.description = lambda : "shows a 3x3 game"
    test.fail = lambda info : "Make sure the game stops when a negative number is entered"
    test.exception = lambda exception : "{}\n{}".format(test.fail(""), str(exception))

@t.test(10)
def shows4x4(test):
    def testMethod():
        import sys
        sys.argv = ["fifteen.py", "4"]
        stdinArgs = ["-1"]
        output = lib.outputOf(_fileName, stdinArgs)
        regex = re.compile(".*"
	      "(15 14 13 12)[ ]*(\n)"
	      "(11 10 09 08)[ ]*(\n)"
	      "(07 06 05 04)[ ]*(\n)"
	      "(03 01 02 __)[ ]*(\n)"
	      ".*", re.MULTILINE)
        return asserts.match(output, regex)

    test.test = testMethod
    test.description = lambda : "shows a 4x4 game"
    test.fail = lambda info : "Make sure the game stops when a negative number is entered"
    test.exception = lambda exception : "{}\n{}".format(test.fail(""), str(exception))

@t.test(40)
def solves3x3(test):
    def testMethod():
        import sys
        sys.argv = ["fifteen.py", "3"]
        stdinArgs = ["3","4","1","2","5","8","7","6","4","1","2","5","8","7","6","4","1","2","4","1","2","3","5","4","7","6","1","2","3","7","4","8","6","4","8","5","7","8","5","6","4","5","6","7","8","6","5","4","7","8"]
        output = lib.outputOf(_fileName, stdinArgs)
        failInfo = output.split("\n")[-5:]
        return asserts.contains(output, "You have won!"), failInfo

    test.test = testMethod
    test.description = lambda : "solves a 3x3 game"
    test.fail = lambda info : "last 5 lines of output:\n{}".format("\n".join(info))

@t.test(50)
def solves4x4(test):
    def testMethod():
        import sys
        sys.argv = ["fifteen.py", "4"]
        stdinArgs = ["4","5","6","1","2","4","5","6","1","2","3","7","11","10","9","1","2","3","4","5","6","8","1","2","3","4","7","11","10","9","14","13","12","1","2","3","4","14","13","12","1","2","3","4","14","13","12","1","2","3","4","12","9","15","1","2","3","4","12","9","13","14","9","13","14","7","5","9","13","14","15","10","11","5","9","13","7","11","5","9","13","7","11","15","10","5","9","13","15","11","8","6","7","8","14","12","6","7","8","14","12","6","7","8","14","15","11","10","6","7","8","12","15","11","10","15","11","14","12","11","15","10","14","15","11","12"]
        output = lib.outputOf(_fileName, stdinArgs)
        failInfo = output.split("\n")[-6:]
        return asserts.contains(output, "You have won!"), failInfo

    test.test = testMethod
    test.description = lambda : "solves a 4x4 game"
    test.fail = lambda info : "last 6 lines of output:\n{}".format("\n".join(info))

@t.test(60)
def invalidInput(test):
    def testMethod():
        import sys
        sys.argv = ["fifteen.py"]
        output = lib.outputOf(_fileName)
        line = lib.getLine(output, 0)
        return asserts.contains(line, "usage: python fifteen.py size")

    test.test = testMethod
    test.description = lambda : "handles lack of argv[1]"

@t.test(70)
def argv1BiggerThan9(test):
    def testMethod():
        import sys
        sys.argv = ["fifteen.py", "10"]
        output = lib.outputOf(_fileName)
        line = lib.getLine(output, 0)
        return asserts.contains(line, "usage: python fifteen.py size")

    test.test = testMethod
    test.description = lambda : "handles argv[1] > 9"

@t.test(80)
def argv1SmallerThan0(test):
    def testMethod():
        import sys
        sys.argv = ["fifteen.py", "-1"]
        output = lib.outputOf(_fileName)
        line = lib.getLine(output, 0)
        return asserts.contains(line, "usage: python fifteen.py size")

    test.test = testMethod
    test.description = lambda : "handles argv[1] < 0"
