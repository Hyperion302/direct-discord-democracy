# Replace error messages with something that makes sense
class UserError(Exception):
	def __init__(self, err_input, message):
		super().__init__(message)
		self.message = message
		self.err_input = err_input

class DatabaseError(Exception):
	def __init__(self, query, message):
		super().__init__(message)
		self.message = message
		self.query = query

class SoftwareError(Exception):
	def __init__(self, message):
		super().__init__(message)
		self.message = message