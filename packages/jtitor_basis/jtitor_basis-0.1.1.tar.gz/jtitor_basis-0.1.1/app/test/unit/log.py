'''Unit tests for log module.
'''

import unittest
from ...setup import Logger, LogLevel

#...How do we test any of this in an automated way?
class LogTest(unittest.TestCase):
	'''Unit tests for log module.
	'''

	def testNormalMethods(self):
		'''Displays all non-contextual methods.
		'''
		testLogger = Logger()

		print("")
		print("You should see the following:")
		print("\t * An entry for info messages")
		print("\t * An entry for warning messages")
		print("\t * An entry for error messages")
		print("\t * An entry for success messages")
		testLogger.info("Info message.")
		testLogger.warning("Warning message.")
		testLogger.error("Error message.")
		testLogger.success("Success message.")

	def testContextMethods(self):
		'''Displays all contextual methods.
		'''
		testLogger = Logger()

		#Verbose and debug depend on context.
		print("")
		testLogger.verbose("You shouldn't be able to see this!")
		testLogger.debug("You shouldn't be able to see this!")

		testLogger._minimumPrintableLevel = LogLevel.Verbose
		print("You should see a verbose message: ")
		testLogger.verbose("Verbose message.")
		print("You should see a debug message: ")
		testLogger.debug("Debug message.")

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(LogTest)
	unittest.TextTestRunner(verbosity=2).run(suite)
