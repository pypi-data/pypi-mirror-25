'''Unit tests for registry module.
'''

import unittest
import platform
from ...setup import Registry

if platform.system() == "Windows":
	try:
		import winreg as _winreg
	except ImportError:
		import _winreg

	class RegistryTest(unittest.TestCase):
		'''Unit tests for registry module.
		'''

		_KeyShouldExist = "SOFTWARE\\"
		_KeyShouldNotExist = "RFUIOUBSEF\\"
		_SubkeyShouldExist = ""

		def testOpenPath(self):
			'''Test Registry.openPath().
			'''

			#Test: valid keys return a key object (not None).
			hKey = _winreg.HKEY_LOCAL_MACHINE
			validWorks = Registry.openPath(hKey, self.__class__._KeyShouldExist) is not None
			if not validWorks:
				print("Valid key {0}{1} could not be opened".format(hKey, self.__class__._KeyShouldExist))
			#Test: invalid keys return None.
			invalidWorks = Registry.openPath(hKey, self.__class__._KeyShouldNotExist) is None
			if not invalidWorks:
				print("Invalid key {0}{1} was somehow opened".format(hKey, self.__class__._KeyShouldNotExist))

			return validWorks and invalidWorks

		#Can't really test this unless there's definitely
		#a MSVC installation on the test system,
		#so not implementing this.
		#def testCheckKeyExists(self):
		#	#	checkKeyExists():
		#	#		* Valid subkeys return True.
		#	#		* Invalid subkeys return False.
		#	raise NotImplementedError()
else:
	#Registry calls will fail/return None if not under Windows,
	#so skip tests in this situation.
	class RegistryTest(unittest.TestCase):
		'''Dummy unit test when running on non-Windows platform.
		'''
		def testRegistry(self):
			'''Dummy test informing tester that this suite is being skipped.
			'''
			print("")
			print("RegistryTest requires Windows, skipping")

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(RegistryTest)
	unittest.TextTestRunner(verbosity=2).run(suite)
