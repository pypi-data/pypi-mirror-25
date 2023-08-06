'''Unit tests for arguments module.
'''

import unittest
from ...setup.arguments import Arguments, Flag, Flags

class Values:
	'''Possible values for a flag.
	'''
	Disable = 0
	Long = 1
	Short = 2
	NumValues = 3

class ArgumentsTest(unittest.TestCase):
	'''Unit tests for arguments module.
	'''

	def _flagValuesToFlagList(self, allFlags, flagValues):
		'''Turns a list of flag visibility values
		into the actual argument list it represents.
		'''
		result = []
		for i in range(0, len(allFlags)):
			value = flagValues[i]
			flag = allFlags[i]
			if value == Values.Long:
				assert flag.value is not None
				result.append(flag.value)
			elif value == Values.Short and flag.shortValue is not None:
				result.append(flag.shortValue)
		return result

	def _parsedValuesMatchFlagValues(self, allFlags, parsedValues, flagValues):
		result = True
		#For each flag:
		for i in range(0, len(allFlags)):
			flag = allFlags[i]
			value = flagValues[i]
			flagSet = value == Values.Long or (value == Values.Short and flag.shortValue is not None)
			#Test: the parsed values set has a field for this flag.
			if(hasattr(parsedValues, flag.name)):
				#Test: if its flag value is set to be visible,
				#	its parsed value is True. Otherwise, the parsed value
				#	is False.
				flagValue = getattr(parsedValues, flag.name)
				if flagValue != flagSet:
					print("Expected flag {0} to have value {1}, got {2}".format(flag.value, flagSet, flagValue))
					result = False
			else:
				print("Parser is missing expected flag {0}".format(flag.value))
				result = False
		return result

	def _validateParseStep(self, allFlags, flagValues, flagIdx, failedFlags):
		if flagIdx >= len(flagValues):
			#Try this combination.
			#Test: combination does not throw.
			combinationThrew = False
			combinationDoesntMatch = False
			args = self._flagValuesToFlagList(allFlags, flagValues)
			try:
				#Test: combination returns expected settings.
				parsedValues = Arguments.parse(args)
				if not self._parsedValuesMatchFlagValues(allFlags, parsedValues, flagValues):
					print("Argument list {0} didn't match expected values".format(args))
					combinationDoesntMatch = True
			except Exception as e:
				print("Argument list {0} threw exception: {1}".format(args, e))
				combinationThrew = True
			#If either happens, add to the failed list.
			if combinationDoesntMatch or combinationThrew:
				failedFlags.append(tuple(flagValues))
		else:
			#Try each value for this flag and recurse.
			for value in range(0, Values.NumValues):
				flagValues[flagIdx] = value
				self._validateParseStep(allFlags, flagValues, flagIdx+1, failedFlags)

	def _validateParse(self, allFlags, flagValues):
		'''Tries all combinations of flags
		and returns any combinations that failed to validate
		as a list of tuples of Values.
		'''
		failedFlags = []
		self._validateParseStep(allFlags, flagValues, 0, failedFlags)
		return failedFlags

	def testParse(self):
		'''Tests that parser works as expected.
		'''

		#Test: try all flags in every order.
		#For a given combination:
		#	* Combination returns expected settings.
		#	* Combination does not throw.
		flagsValidated = False
		allFlags = Flags.AllBoolean
		flagValues = [Values.Disable] * len(allFlags)
		failedFlags = self._validateParse(allFlags, flagValues)
		flagsValidated = len(failedFlags) < 1

		#Test: Make sure invalid combinations raise an exception.
		invalidFlagsValidated = False
		try:
			invalidFlags = ["--ofsjis", "-0", "swfk28"]
			#TODO: Supress parser errors if verbose test is disabled?
			Arguments.parse(invalidFlags)
			print("Failure: Arguments.parse() didn't raise an exception on invalid input")
		#Oddly enough, this fails if an exception type is specified.
		#pylint: disable=W0702
		except:
			invalidFlagsValidated = True

		self.assertTrue(flagsValidated and invalidFlagsValidated)

	def testExtraFlags(self):
		'''Tests that the extra flags option works.
		'''

		extraFlagName = "extra-flag"
		extraFlag = Flag("Test extra flag.", extraFlagName)
		#Make sure it's set to true when passed in the parse.
		parsedArgs = Arguments.parse([extraFlag.value], (extraFlag,))
		self.assertTrue(parsedArgs.extra_flag,
			"Extra flag '{0}' should be set but isn't".format(extraFlag.value))

if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(ArgumentsTest)
	unittest.TextTestRunner(verbosity=2).run(suite)
