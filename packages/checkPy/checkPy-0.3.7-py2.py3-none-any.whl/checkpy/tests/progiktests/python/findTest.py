import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as asserts

@t.test(0)
def findsBegin(test):
	def testMethod():
		import sys
		sys.argv = ["find.py", "28", "28", "29", "30"]
		output = lib.outputOf(_fileName)
		line = lib.getLine(output, 0)
		return asserts.contains(line, "Found the needle")

	test.test = testMethod
	test.description = lambda : "finds 28 in 28,29,30"

@t.test(10)
def findsMiddle(test):
	def testMethod():
		import sys
		sys.argv = ["find.py", "28", "27", "28", "29"]
		output = lib.outputOf(_fileName)
		line = lib.getLine(output, 0)
		return asserts.contains(line, "Found the needle")

	test.test = testMethod
	test.description = lambda : "finds 28 in 27,28,29"

@t.test(20)
def findsEnd(test):
	def testMethod():
		import sys
		sys.argv = ["find.py", "28", "27", "28", "29"]
		output = lib.outputOf(_fileName)
		line = lib.getLine(output, 0)
		return asserts.contains(line, "Found the needle")

	test.test = testMethod
	test.description = lambda : "finds 28 in 26,27,28"

@t.test(30)
def findsLeftMiddle(test):
	def testMethod():
		import sys
		sys.argv = ["find.py", "28", "27", "28", "29", "30"]
		output = lib.outputOf(_fileName)
		line = lib.getLine(output, 0)
		return asserts.contains(line, "Found the needle")

	test.test = testMethod
	test.description = lambda : "finds 28 in 27,28,29,30"

@t.test(40)
def findsRightMiddle(test):
	def testMethod():
		import sys
		sys.argv = ["find.py", "28", "26", "27", "28", "29"]
		output = lib.outputOf(_fileName)
		line = lib.getLine(output, 0)
		return asserts.contains(line, "Found the needle")

	test.test = testMethod
	test.description = lambda : "finds 28 in 26,27,28,29"

@t.test(50)
def findsEnd4(test):
	def testMethod():
		import sys
		sys.argv = ["find.py", "28", "25", "26", "27", "28"]
		output = lib.outputOf(_fileName)
		line = lib.getLine(output, 0)
		return asserts.contains(line, "Found the needle")

	test.test = testMethod
	test.description = lambda : "finds 28 in 25,26,27,28"

@t.test(60)
def notFind3(test):
	def testMethod():
		import sys
		sys.argv = ["find.py", "28", "25", "26", "27"]
		output = lib.outputOf(_fileName)
		line = lib.getLine(output, 0)
		return asserts.contains(line, "Did not find the needle")

	test.test = testMethod
	test.description = lambda : "doesn't find 28 in 25,26,27"

@t.test(70)
def notFind4(test):
	def testMethod():
		import sys
		sys.argv = ["find.py", "28", "25", "26", "27", "29"]
		output = lib.outputOf(_fileName)
		line = lib.getLine(output, 0)
		return asserts.contains(line, "Did not find the needle")

	test.test = testMethod
	test.description = lambda : "doesn't find 28 in 25,26,27,29"

@t.test(80)
def findsRandom(test):
	def testMethod():
		import sys
		sys.argv = ["find.py", "28", "30", "27", "28", "26"]
		output = lib.outputOf(_fileName)
		line = lib.getLine(output, 0)
		return asserts.contains(line, "Found the needle")

	test.test = testMethod
	test.description = lambda : "finds 28 in 30,27,28,26"
