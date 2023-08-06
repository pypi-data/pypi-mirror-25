import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as asserts
import re

@t.test(10)
def height0(test):
	def testMethod():
		stdinArgs = [0]
		output = lib.outputOf(_fileName, stdinArgs)
		return not asserts.contains(output, "#")

	test.test = testMethod
	test.description = lambda : "handles a height of 0 correctly"

@t.test(20)
def height1(test):
	def testMethod():
		stdinArgs = [1]
		output = lib.outputOf(_fileName, stdinArgs)
		regex = re.compile(".*"
	      "(##)[ ]*"
	      ".*", re.MULTILINE)
		return asserts.match(output, regex)

	test.test = testMethod
	test.description = lambda : "handles a height of 1 correctly"

@t.test(30)
def height2(test):
	def testMethod():
		stdinArgs = [2]
		output = lib.outputOf(_fileName, stdinArgs)
		regex = re.compile(".*"
			"( ##)[ ]*(\n)"
			"(###)[ ]*"
			".*", re.MULTILINE)
		return asserts.match(output, regex)

	test.test = testMethod
	test.description = lambda : "handles a height of 2 correctly"

@t.test(30)
def height23(test):
	def testMethod():
		stdinArgs = [23]
		output = lib.outputOf(_fileName, stdinArgs)
		regex = re.compile(".*"
			"(                      ##)[ ]*(\n)"
			"(                     ###)[ ]*(\n)"
			"(                    ####)[ ]*(\n)"
			"(                   #####)[ ]*(\n)"
			"(                  ######)[ ]*(\n)"
			"(                 #######)[ ]*(\n)"
			"(                ########)[ ]*(\n)"
			"(               #########)[ ]*(\n)"
			"(              ##########)[ ]*(\n)"
			"(             ###########)[ ]*(\n)"
			"(            ############)[ ]*(\n)"
			"(           #############)[ ]*(\n)"
			"(          ##############)[ ]*(\n)"
			"(         ###############)[ ]*(\n)"
			"(        ################)[ ]*(\n)"
			"(       #################)[ ]*(\n)"
			"(      ##################)[ ]*(\n)"
			"(     ###################)[ ]*(\n)"
			"(    ####################)[ ]*(\n)"
			"(   #####################)[ ]*(\n)"
			"(  ######################)[ ]*(\n)"
			"( #######################)[ ]*(\n)"
			"(########################)[ ]*(\n)"
			".*", re.MULTILINE)
		return asserts.match(output, regex)

	test.test = testMethod
	test.description = lambda : "handles a height of 23 correctly"

@t.test(50)
def rejectMinus1(test):
	def testMethod():
		stdinArgs = [-1, 0]
		output = lib.outputOf(_fileName, stdinArgs)
		return not asserts.contains(output, "#")

	test.test = testMethod
	test.description = lambda : "rejects a height of -1 and then accepts a height of 0"

@t.test(60)
def reject24(test):
	def testMethod():
		stdinArgs = [24, 2]
		output = lib.outputOf(_fileName, stdinArgs)
		regex = re.compile(".*"
			"( ##)[ ]*(\n)"
			"(###)[ ]*"
			".*", re.MULTILINE)
		return asserts.match(output, regex)

	test.test = testMethod
	test.description = lambda : "rejects a height of 24 and then accepts a height of 2"
