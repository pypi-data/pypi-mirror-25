'''Unit tests for context module.
'''

import unittest
import platform
from ...setup.context import Context, Logger

class ContextTest(unittest.TestCase):
	'''Unit tests for context module.
	'''

	def testDefaultValidity(self):
		'''Tests that a default-constructed
		Context is valid on this platform.
		'''
		logger = Logger()
		ctx = Context(logger)
		self.assertTrue(ctx.isValid)

	def testContextDisplay(self):
		'''Tests the two context display methods.
		'''
		logger = Logger()
		ctx = Context(logger)
		print("")
		print("Context full display:")
		ctx.printContextDescription()
		print("Context summary:")
		ctx.printContextSummary()

	def testOSQuery(self):
		'''Tests that Context.osIs*() methods
		return their expected values.
		'''

		#Not really useful, since Context
		#basically uses os.platform directly for this.
		passed = True
		logger = Logger()
		ctx = Context(logger)
		expectedResults = (platform.system() == "Windows",
			platform.system() == "Linux",
			platform.system() == "Darwin")
		methodsToTest = (ctx.osIsWindows, ctx.osIsLinux, ctx.osIsMacOS)
		for i in range(0, len(expectedResults)):
			currExpectedResult = expectedResults[i]
			currMethod = methodsToTest[i]
			actualResult = currMethod()
			if actualResult != currExpectedResult:
				passed = False
				print("Expected {0}() to return {1}, got {2}".format(currMethod.__name__,
					currExpectedResult, actualResult))

		self.assertTrue(passed)

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(ContextTest)
	unittest.TextTestRunner(verbosity=2).run(suite)
