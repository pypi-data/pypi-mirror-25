'''Runs all tests for basis.
'''

import unittest
from .test.integration import IntegrationTest
from .test.unit.all import AllUnitTest

def suite():
	'''Returns all tests for basis.
	'''
	return unittest.TestSuite([AllUnitTest.suite(), IntegrationTest.suite()])

def main():
	unittest.TextTestRunner(verbosity=2).run(suite())

if __name__ == "__main__":
	main()
