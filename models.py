class User(netID):

	@property
	def is_authenticated():
		return True

	@property
	def is_active():
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)