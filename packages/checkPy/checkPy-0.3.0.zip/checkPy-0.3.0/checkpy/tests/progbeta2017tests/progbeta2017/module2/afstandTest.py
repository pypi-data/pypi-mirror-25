import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib

@t.test(10)
def hasVierkant(test):
	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "vierkant")
	test.description = lambda : "definieert de functie vierkant()"

@t.passed(hasVierkant)
@t.test(11)
def correctVierkant(test):
	test.test = lambda : assertlib.between(lib.getFunction("vierkant", _fileName)(), 0.51, 0.54)
	test.description = lambda : "vierkant geeft de goede afstand terug"