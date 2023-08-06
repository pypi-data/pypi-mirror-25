'''Operations on the Windows registry.
'''

#Don't define any of this if we're not running under Windows.
try:
	from .version import Version
	try:
		import winreg as _winreg
	except ImportError:
		import _winreg

	###
	# WINDOWS REGISTRY OPERATIONS
	###
	class Registry(object):
		'''Allows operations on the Windows registry.
		On a non-Windows platform this class' methods do nothing.
		'''

		@classmethod
		def openPath(cls, hKey, keyPath):
			'''Opens the specified key if possible.
			'''

			try:
				return _winreg.OpenKey(hKey, keyPath, 0, _winreg.KEY_READ)
			except WindowsError:
				return None

		@classmethod
		def checkKeyExists(cls, key32, key64, minVersion):
			'''Determines if a subkey >= minVersion exists
			in the given key. minVersion must be a Version object.
			key32 is used first, then key64 if key32 couldn't be found.
			Returns:
				* True if a viable subkey was found.
				* False if key32 and key64 don't exist, or
				no viable subkey could be found.
			'''

			hKey = _winreg.HKEY_LOCAL_MACHINE
			#See if the 32 bit key exists.
			key = Registry.openPath(hKey, key32)
			#Else, see if the 64 bit key exists.
			if key is None:
				key = Registry.openPath(hKey, key64)
			#Otherwise we abort here.
			if key is None:
				return False

			subkeys = []
			#Now enumerate the subkeys...
			subIdx = 0
			while True:
				try:
					subkeys.append(_winreg.EnumKey(key, subIdx))
					subIdx += 1
				except WindowsError:
					break

			#Search for one equal to or over the minimum version.
			for subkeyPath in subkeys:
				try:
					subkeyVersion = Version(subkeyPath)
					if subkeyVersion >= minVersion:
						return True
				except Exception:
					pass
			return False

except ImportError:
	class Registry(object):
		'''Dummy implementation of Registry for
		non-Windows platforms. All methods do nothing.
		'''
		@classmethod
		def openPath(cls, *_):
			'''Does nothing.
			'''
			return None

		@classmethod
		def checkKeyExists(cls, *_):
			'''Does nothing.
			'''
			return False
