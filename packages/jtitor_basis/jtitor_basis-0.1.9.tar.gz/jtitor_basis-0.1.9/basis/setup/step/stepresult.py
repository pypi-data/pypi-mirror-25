class StepResultCategory(object):
	'''Specifies what kind of result a result is.
	'''

	'''The operation could not be completed; during a check,
	indicates that the operation should be performed.
	'''
	Fail = 0
	'''The operation was successfully performed; during a check,
	indicates that the operation does not need to be performed.
	'''
	Success = 1
	'''The operation was not performed at all; during a check,
	indicates that the operation does not need to be performed.
	'''
	Skip = 2
	Count = 3
	Descriptions = ("Step failed",
					"Step succeeded",
					"Step skipped")

class StepResultReason(object):
	'''Specifies why a result occurred.
	'''

	'''Unspecified failure.
	'''
	Fail = 0
	'''Step has not yet been performed.
	'''
	NotDone = 1
	'''The step must always be performed; there is no way to skip this or mark as already done.
	'''
	Mandatory = 2
	'''Something the step relies on does not
	have the right version.
	'''
	WrongVersion = 3
	'''Unspecified success.
	'''
	Success = 4
	'''The step was successfully performed
	and installed new software.
	'''
	Installed = 5
	'''The requirements for the step have already been met.
	'''
	AlreadyDone = 6
	'''The system has the wrong platform for this step,
	and the step is optional.
	'''
	Unnecessary = 7
	Count = 8
	'''Human-readable descriptions for each step.
	'''
	Descriptions = ("Unspecified failure",
						"Not yet performed",
						"Mandatory",
						"Wrong version",
						"Unspecified success",
						"Installed",
						"Already done",
						"Unnecessary")
	'''What type of result this reason belongs to.
	'''
	ToCategory = (StepResultCategory.Fail,
					StepResultCategory.Fail,
					StepResultCategory.Fail,
					StepResultCategory.Fail,
					StepResultCategory.Success,
					StepResultCategory.Success,
					StepResultCategory.Skip,
					StepResultCategory.Skip)

class StepResultObject(object):
	'''Describes the result of an operation on a step.
	'''

	def __init__(self, reason):
		if reason < 0 or reason >= StepResultReason.Count:
			raise RuntimeError("StepResult must have reason in range [0,{0})".format(StepResultReason.Count))
		'''The overall value category of the result.
		'''
		self.category = StepResultReason.ToCategory[reason]
		'''The reason for the result.
		'''
		self.reason = reason
		'''A human-readable description of the result.
		'''
		self.description = StepResultReason.Descriptions[self.reason]

	def __repr__(self):
		return "{0} ({1})".format(StepResultCategory.Descriptions[self.category], self.description)

	def __bool__(self):
		return self.category != StepResultCategory.Fail
	#Python 2 uses __nonzero__ instead.
	__nonzero__ = __bool__

	def __eq__(self, other):
		if isinstance(other, StepResultObject):
			return self.category == other.category and self.reason == other.reason
		return False

	def __ne__(self, other):
		return not self.__eq__(other)

class StepResult(object):
	'''Predefined results.
	'''

	'''Unspecified failure.
	'''
	Fail = StepResultObject(StepResultReason.Fail)
	'''The step has not been performed and must be performed.
	'''
	NotDone = StepResultObject(StepResultReason.NotDone)
	'''The step must always be performed; there is no way to skip this or mark as already done.
	'''
	Mandatory = StepResultObject(StepResultReason.Mandatory)
	'''The system has the wrong version installed.
	'''
	WrongVersion = StepResultObject(StepResultReason.WrongVersion)
	'''Unspecified success.
	'''
	Success = StepResultObject(StepResultReason.Success)
	'''The operation was performed and installed new software.
	'''
	Installed = StepResultObject(StepResultReason.Installed)
	'''The operation was skipped since it already seems to have been performed.
	'''
	AlreadyDone = StepResultObject(StepResultReason.AlreadyDone)
	'''The operation was skipped since it was unnecessary.
	'''
	Unnecessary = StepResultObject(StepResultReason.Unnecessary)

	@classmethod
	def fromBool(cls, value):
		'''Returns the result for each boolean value.
		True maps to Success, False to Fail.
		'''

		if value:
			return cls.Success
		return cls.Fail
