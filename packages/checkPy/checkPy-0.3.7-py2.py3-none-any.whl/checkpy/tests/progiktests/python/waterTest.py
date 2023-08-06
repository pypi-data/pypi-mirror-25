import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as asserts

@t.test(10)
def water1(test):
	def testMethod():
		stdinArgs = [1]
		output = lib.outputOf(_fileName, stdinArgs)
		return asserts.contains(output, "12")

	test.test = testMethod
	test.description = lambda : "1 minute equals 12 bottles."

@t.test(20)
def water2(test):
	def testMethod():
		stdinArgs = [2]
		output = lib.outputOf(_fileName, stdinArgs)
		return asserts.contains(output, "24")

	test.test = testMethod
	test.description = lambda : "2 minutes equals 24 bottles."

@t.test(30)
def water5(test):
	def testMethod():
		stdinArgs = [5]
		output = lib.outputOf(_fileName, stdinArgs)
		return asserts.contains(output, "60")

	test.test = testMethod
	test.description = lambda : "5 minutes equals 60 bottles."

@t.test(40)
def water10(test):
	def testMethod():
		stdinArgs = [10]
		output = lib.outputOf(_fileName, stdinArgs)
		return asserts.contains(output, "120")

	test.test = testMethod
	test.description = lambda : "10 minutes equals 120 bottles."