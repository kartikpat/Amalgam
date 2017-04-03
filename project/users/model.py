class User(object):
	
    __name = ""
    __email = ""
    __password = ""

	def __init__(self, arg):
		super(User, self).__init__()
		self.arg = arg
		