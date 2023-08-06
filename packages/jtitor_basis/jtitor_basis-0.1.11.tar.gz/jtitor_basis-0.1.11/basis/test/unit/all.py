'''Runs all unit tests.
'''

import unittest
from .arguments import ArgumentsTest
from .context import ContextTest
from .log import LogTest
from .registry import RegistryTest
from .step.stepbase import StepExecutorTest
from .step.shellmanager import ShellManagerTest
from .step.packagemanager import PackageManagerTest
from .version import VersionTest

class AllUnitTest:
	'''Runs all unit tests.
	'''

	@classmethod
	def suite(cls):
		'''Returns all unit tests.
		'''

		allCases = (ArgumentsTest,
			ContextTest,
			LogTest,
			RegistryTest,
			StepExecutorTest,
			ShellManagerTest,
			PackageManagerTest,
			VersionTest)
		allSuites = []

		for case in allCases:
			allSuites.append(unittest.TestLoader().loadTestsFromTestCase(case))

		return unittest.TestSuite(allSuites)

if __name__ == "__main__":
	unittest.TextTestRunner(verbosity=2).run(AllUnitTest.suite())
