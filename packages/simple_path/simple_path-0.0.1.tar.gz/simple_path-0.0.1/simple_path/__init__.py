import os
import copy as copy_module

# The module version.
version = "0.0.1"

class path():
	""" Library to abstract paths, Mostly act's like a list with a few helper functions. """
	# Just to note, I wish I could just subclass list...

	def __init__(self, relative = False):
		""" Initilizes the class. """
		# The list we keep the sections in.
		self.list = list()
		# What the path starts with.
		self.pathstart = os.path.abspath(os.sep)
		# Allow for relative paths.
		self.relative = relative

	def remove(self, *args):
		""" Deletes a section from the path. """
		return self.list.remove(*args)

	def insert(self, *args):
		return self.list.insert(*args)

	def append(self, *args):
		return self.list.append(*args)

	def to_str(self, strip_end_sep = True):
		""" Converts a path object to a filesystem string. """
		return_string = self.pathstart

		# Put together the string.
		for section in self.list:
			return_string = return_string + section + os.path.sep

		# Stirp the leading path seperator.
		if self.relative:
			return_string = return_string.lstrip(os.path.sep)

		# Strip the ending path seperator.
		if strip_end_sep:
			return_string = return_string.rstrip(os.path.sep)

		# Return it.
		return return_string

	def from_str(self, string):
		""" Converts a filesystem string to a path object. """
		split_string = string.split(os.path.sep)

		# Add each chunk.
		for each in split_string:
			if each == "":
				continue
			self.append(each)

	def copy(self):
		""" Returns a copy of self. """
		return copy_module.deepcopy(self)

	def __add__(self, other):
		""" Return self + other. """
		# If we're being added to a string, return us as a string.
		if type(other) is str:
			return self.to_str() + other
		# If we're being added to another like self, then return a copy of self with the other one added to it
		elif isinstance(other, type(self)):
			tmp = self.copy()
			tmp.list = tmp.list + other.list
			return tmp
		else:
			# Catch-all for other objects.
			raise Exception("Unsupported object!")


	def __radd__(self, other):
		""" Return value + self. """
		# If we're being added to a string, return us as a string.
		if type(other) is str:
			return other + self.to_str()
		# If we're being added to another like self, then return a copy of self with the other one added to it.
		elif isinstance(other, type(self)):
			tmp = self.copy()
			tmp.list = other.list + tmp.list
			return tmp
		else:
			# Catch-all for other objects.
			raise Exception("Unsupported object!")

	def __repr__(self):
		""" Return a printable representation of self. """
		return self.list.__repr__()

	def __delitem__(self, key):
		""" Delete self[key]. """
		return self.list.__delitem__(key)

	def __getitem__(self, key):
		""" Return self[key]. """
		return self.list.__getitem__(key)

	def __setitem__(self, key, value):
		""" Self self[key] to value. """
		return self.list.__setitem__(key, value)

	def __len__(self):
		""" Return len(self). """
		return self.list.__len__()

	def __getattr__(self, attr):
		""" Return getattr(self.list, name). """
		# Pass all unknown functions/variables to the list.
		# That is if they don't exist here already.
		return getattr(self.list, attr)
