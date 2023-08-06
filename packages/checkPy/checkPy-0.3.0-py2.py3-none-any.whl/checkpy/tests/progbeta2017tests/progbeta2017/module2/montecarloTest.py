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
def hasMontecarlo(test):
	test.test = lambda : assertlib.fileContainsFunctionDefinitions(_fileName, "montecarlo")
	test.description = lambda : "definieert de functie montecarlo()"

@t.passed(hasMontecarlo)
@t.test(1)
def correctFunc1(test):
	test.test = lambda : assertlib.between(lib.getFunction("montecarlo", _fileName)(lambda x : x**(x + 0.5), 0, 0, 1, 1), 0.51, 0.54)
	test.description = lambda : "montecarlo werkt correct voor x^(x + 0.5) van x1=0, y1=0 tot x2=1, y2=1"

@t.passed(hasMontecarlo)
@t.test(2)
def correctFunc2(test):
	test.test = lambda : assertlib.between(lib.getFunction("montecarlo", _fileName)(lambda x : math.tan(math.cos(math.sin(x))), 0.2, 0, 2.2, 1.5), 1.69, 1.73)
	test.description = lambda : "montecarlo werkt correct voor tan(cos(sin(x))) van x1=0.2, y1=0 tot x2=2.2, y2=1.5"

@t.passed(hasMontecarlo)
@t.test(3)
def correctFunc3(test):
	test.test = lambda : assertlib.between(lib.getFunction("montecarlo", _fileName)(lambda x : math.sin(x**2), 0, -1, math.pi, 1), 0.75, 0.79)
	test.description = lambda : "montecarlo werkt correct voor sin(x^2) van x1=0, y1=-1 tot x2=pi, y2=1"