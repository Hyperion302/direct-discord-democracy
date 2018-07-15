# Replace error messages with something that makes sense
class InputError(Exception):
	def __init__(self, input_segment):
		super().__init__("Something you said didn't make sense")
		self.input_segment = input_segment

class DatabaseError(Exception):
	def __init__(self, error):
		super().__init__("Could not read database")
		self.error = error

class UserNotFoundError(Exception):
	def __init__(self, userQuery):
		super().__init__("User not found")
		self.userQuery = userQuery

class DocNotFoundError(Exception):
	def __init__(self, query):
		super().__init__("Doc not found")
		self.query = query