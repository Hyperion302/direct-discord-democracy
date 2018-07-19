# Replace error messages with something that makes sense
class UserError(Exception):
	def __init__(self, input_segment):
		super().__init__("There was an error with your command")
		self.input_segment = input_segment

class DatabaseError(Exception):
	def __init__(self, error):
		super().__init__("The database could not be reached")
		self.error = error

class SoftwareError(Exception):
	def __init__(self, userQuery):
		super().__init__("An unexpected error occured in the backend")
		self.userQuery = userQuery