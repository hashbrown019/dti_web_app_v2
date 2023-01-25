
class inbound(object):
	"""docstring for inbound"""
	def __init__(self, app_):
		super(inbound, self).__init__()
		self.app_ = app_
		
	def _test_(self):
		print(" * Testing Inbound | {}".format(self.app_))
		pass