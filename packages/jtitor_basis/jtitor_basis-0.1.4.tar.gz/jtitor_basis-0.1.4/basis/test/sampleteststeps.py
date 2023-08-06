'''Dummy steps that return specified values.
'''

from ..setup import StepResult

class TestSteps(object):
	'''Valid dummy steps that return specified values.
	'''

	class Pass(object):
		'''Represents an operation
		that had to be performed and was done successfully.
		'''
		Name = "This step should pass installation"

		@classmethod
		def check(cls, _):
			'''Dummy check. Does nothing.
			'''
			return StepResult.NotDone

		@classmethod
		def run(cls, _):
			'''Dummy run. Does nothing.
			'''
			return StepResult.Success

	class Fail(object):
		'''Represents an operation
		that had to be performed but failed installation.
		'''
		Name = "This step should fail installation"

		@classmethod
		def check(cls, _):
			'''Dummy check. Does nothing.
			'''
			return StepResult.NotDone

		@classmethod
		def run(cls, _):
			'''Dummy run. Does nothing.
			'''
			return StepResult.Fail

	class Installed(object):
		'''Represents an operation
		that was already performed?
		TODO: Should we remove StepResult.Installed? How is this different from Success in practice?
		'''
		Name = "This step should be marked as installed"

		@classmethod
		def check(cls, _):
			'''Dummy check. Does nothing.
			'''
			return StepResult.Installed

		@classmethod
		def run(cls, _):
			'''Dummy run. Does nothing.
			'''
			return StepResult.Installed

	class Unnecessary(object):
		'''Represents an operation
		that was unnecessary and was skipped.
		'''
		Name = "This step should be skipped as unnecessary"

		@classmethod
		def check(cls, _):
			'''Dummy check. Does nothing.
			'''
			return StepResult.Unnecessary

		@classmethod
		def run(cls, _):
			'''Dummy run. Does nothing.
			'''
			return StepResult.Unnecessary

	class AlreadyDone(object):
		'''Represents an operation
		that was already performed and skipped.
		'''
		Name = "This step should be skipped as already being done"

		@classmethod
		def check(cls, _):
			'''Dummy check. Does nothing.
			'''
			return StepResult.AlreadyDone

		@classmethod
		def run(cls, _):
			'''Dummy run. Does nothing.
			'''
			return StepResult.AlreadyDone

	class NotDone(object):
		'''Represents an operation
		that had to be performed and was done successfully.
		TODO: Again, how is this different from TestSteps.Pass?
		'''
		Name = "This step should be checked as not done and run"

		@classmethod
		def check(cls, _):
			'''Dummy check. Does nothing.
			'''
			return StepResult.NotDone

		@classmethod
		def run(cls, _):
			'''Dummy run. Does nothing.
			'''
			print("In NotDone.run()")
			return StepResult.Success

	class WrongVersion(object):
		'''Represents an operation
		that had to be performed because the
		asset involved has the wrong version.
		'''
		Name = "This step should be checked as wrong version and run"

		@classmethod
		def check(cls, _):
			'''Dummy check. Does nothing.
			'''
			return StepResult.WrongVersion

		@classmethod
		def run(cls, _):
			'''Dummy run. Does nothing.
			'''
			print("In WrongVersion.run()")
			return StepResult.Success

class AnomalousSteps(object):
	'''These steps all have something
	that should cause an error or warning.
	'''
	class Nameless(object):
		'''Step is missing its name,
		but is otherwise valid.
		'''

		@classmethod
		def check(cls, _):
			'''Dummy check. Does nothing.
			'''
			return StepResult.NotDone

		@classmethod
		def run(cls, _):
			'''Dummy run. Does nothing.
			'''
			print("In WrongVersion.run()")
			return StepResult.Success
