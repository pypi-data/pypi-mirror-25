import checkpy.tests as t
import checkpy.lib as lib
import checkpy.assertlib as assertlib
import math

def before():
	import matplotlib.pyplot as plt
	plt.switch_backend("Agg")
	lib.neutralizeFunction(plt.pause)

def after():
	import matplotlib.pyplot as plt
	plt.switch_backend("TkAgg")
	reload(plt)

@t.test(0)
def hasRiemann(test):
	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "riemann")
	test.description = lambda : "definieert de functie riemann()"

@t.passed(hasRiemann)
@t.test(1)
def correctFunc1(test):
	test.test = lambda : assertlib.between(lib.getFunction("riemann", _fileName)(lambda x : x**(x + 0.5), 0, 1, 10000), 0.52, 0.53)
	test.description = lambda : "riemann werkt correct voor x^(x + 0.5) van a=0 tot b=1 met n=10000"

@t.passed(hasRiemann)
@t.test(2)
def correctFunc2(test):
	test.test = lambda : assertlib.between(lib.getFunction("riemann", _fileName)(lambda x : math.tan(math.cos(math.sin(x))), 0.2, 2.2, 10000), 1.70, 1.71)
	test.description = lambda : "riemann werkt correct voor tan(cos(sin(x))) van a=0.2 tot b=2.2 met n=10000"

@t.passed(hasRiemann)
@t.test(3)
def correctFunc3(test):
	test.test = lambda : assertlib.between(lib.getFunction("riemann", _fileName)(lambda x : math.sin(x**2), 0, math.pi, 10000), 0.77, 0.78)
	test.description = lambda : "riemann werkt correct voor sin(x^2) van a=0 tot b=pi met n=10000"