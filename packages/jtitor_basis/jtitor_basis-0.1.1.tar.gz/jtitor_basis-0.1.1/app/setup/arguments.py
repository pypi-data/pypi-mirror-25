'''Argument parsing system and classes.
'''

import argparse

class Flag(object):
	'''Represents a boolean flag.
	'''

	def __init__(self, description, value, shortValue=None):
		self.description = None
		self.name = None
		self.value = None
		self.shortValue = None
		if value is None or len(value) < 1:
			raise RuntimeError("Can't make a flag without a value")
		#Convert any dashes in the name to underscores
		#so it is a valid Python variable.
		self.name = value.replace("-", "_")
		if len(value) > 1:
			self.value = "--{0}".format(value)
		else:
			self.value = "-{0}".format(value)
		if shortValue is not None and len(shortValue) == 1 and shortValue != value:
			self.shortValue = "-{0}".format(shortValue)
		self.description = description

	def valueList(self):
		'''Returns all valid aliases for this flag.
		'''

		results = []
		if self.value is not None:
			results.append(self.value)
		if self.shortValue is not None:
			results.append(self.shortValue)
		return results

def _addBooleanFlags(parser, flags):
	for f in flags:
		parser.add_argument(*f.valueList(),
			action="store_true",
			help=f.description)

#Parsing constants.
class Flags(object):
	'''Predefined flags.
	'''
	_CheckOnlyDesc = "Makes installer only check for installed tools. Takes precedence over --verify."
	CheckOnly = Flag(_CheckOnlyDesc, "check-only", "c")
	Verbose = Flag("Enables verbose output.", "verbose", "v")
	Debug = Flag("Enables debug output.", "debug", "d")
	Verify = Flag("Runs a check after installation. Does nothing if --check-only is set.", "verify")
	PermitWarnings = Flag("If set, warning exceptions are not thrown", "permit-warnings", "p")
	AllBoolean = [CheckOnly, Verbose, Debug, Verify, PermitWarnings]

class Arguments(object):
	'''Parses command-line arguments.
	'''

	ProgramDescription = "Installs needed tools to build the product."
	ParserInitialized = False
	Parser = argparse.ArgumentParser(description=ProgramDescription)

	@classmethod
	def getParser(cls):
		'''Gets an instance of the parser.
		'''

		parser = cls.Parser
		if not cls.ParserInitialized:
			_addBooleanFlags(parser, Flags.AllBoolean)
			cls.ParserInitialized = True
		return parser

	@classmethod
	def parse(cls, args=None, extraFlags=()):
		'''Performs an argparse with the defined flags on
		the given argument list.
		Returns an argparse result object.
		'''

		parser = cls.getParser()
		#Add any extra arguments as needed.
		_addBooleanFlags(parser, extraFlags)
		result = None
		if args is None:
			result = parser.parse_args()
		else:
			result = parser.parse_args(args)
		return result
