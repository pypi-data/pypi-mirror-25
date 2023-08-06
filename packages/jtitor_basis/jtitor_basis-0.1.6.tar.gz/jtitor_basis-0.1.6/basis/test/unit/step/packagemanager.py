'''Unit tests for packagemanager module.
'''

import unittest
from ....setup import Context
from ....setup import PackageManager, ShellManager
from ....setup import Logger

class PackageManagerTest(unittest.TestCase):
	'''Unit tests for packagemanager module.
	'''

	def testPackageCommands(self):
		'''Tests package management methods.
		'''

		print("")
		logger = Logger()
		ctx = Context(logger)
		if ctx.osIsWindows():
			print("Package test needs non-Windows OS, skipping")
		else:
			package = PackageManager(ShellManager(ctx, logger), logger)
			packageToCheck = "emacs"
			#Don't actually want to modify the system, so just
			#check that the package check doesn't give an exception.
			print("Package check tool: " + package.context.packageCheckInstalledTool)
			package.checkInstalled(packageToCheck)

	#TODO: can we test MSI installation?

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(PackageManagerTest)
	unittest.TextTestRunner(verbosity=2).run(suite)
