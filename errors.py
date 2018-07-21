# Replace error messages with something that makes sense
class UserError(Exception):
	def __init__(self, err_input):
		super().__init__("There was an error with your command")
		self.err_input = err_input

class DatabaseError(Exception):
	def __init__(self, query):
		super().__init__("The database could not be reached")
		self.query = query

class SoftwareError(Exception):
	def __init__(self, error):
		super().__init__("An unexpected error occured in the backend")
		self.error = error