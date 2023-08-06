import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as asserts

@t.test(0)
def yields41(test):
	def testMethod():
		stdinArgs = [0.41]
		output = lib.outputOf(_fileName, stdinArgs)
		line = lib.getLine(output, 0)
		return asserts.numberOnLine(4, line)

	test.test = testMethod
	test.description = lambda : "input of 0.41 yields output of 4"

@t.test(10)
def yields1(test):
	def testMethod():
		stdinArgs = [0.01]
		output = lib.outputOf(_fileName, stdinArgs)
		line = lib.getLine(output, 0)
		return asserts.numberOnLine(1, line)

	test.test = testMethod
	test.description = lambda : "input of 0.01 yields output of 1"

@t.test(20)
def yields15(test):
	def testMethod():
		stdinArgs = [0.15]
		output = lib.outputOf(_fileName, stdinArgs)
		line = lib.getLine(output, 0)
		return asserts.numberOnLine(2, line)

	test.test = testMethod
	test.description = lambda : "input of 0.15 yields output of 2"

@t.test(30)
def yields160(test):
	def testMethod():
		stdinArgs = [1.60]
		output = lib.outputOf(_fileName, stdinArgs)
		line = lib.getLine(output, 0)
		return asserts.numberOnLine(7, line)

	test.test = testMethod
	test.description = lambda : "input of 1.60 yields output of 7"

@t.test(40)
def yields2300(test):
	def testMethod():
		stdinArgs = [23]
		output = lib.outputOf(_fileName, stdinArgs)
		line = lib.getLine(output, 0)
		return asserts.numberOnLine(92, line)

	test.test = testMethod
	test.description = lambda : "input of 23 yields output of 92"

@t.test(50)
def yields420(test):
	def testMethod():
		stdinArgs = [4.20]
		output = lib.outputOf(_fileName, stdinArgs)
		line = lib.getLine(output, 0)
		return asserts.numberOnLine(18, line)

	test.test = testMethod
	test.description = lambda : "input of 4.2 yields output of 18"

@t.test(60)
def rejectNegative(test):
	def testMethod():
		stdinArgs = [-1, 0.01]
		output = lib.outputOf(_fileName, stdinArgs)
		line = lib.getLine(output, 0)
		return asserts.numberOnLine(1, line)

	test.test = testMethod
	test.description = lambda : "rejects a negative input of -1 and then accepts an input of 0.01"
