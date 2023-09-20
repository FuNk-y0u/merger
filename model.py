from inc import *

pdb = SQLAlchemy()

	
class User(pdb.Model, UserMixin):
	id            = pdb.Column(pdb.String(128), primary_key=True)
	email         = pdb.Column(pdb.String(50))
	username      = pdb.Column(pdb.String(50))
	is_verified   = pdb.Column(pdb.Boolean, default = False)
	password_hash = pdb.Column(pdb.String(250))
	password_salt = pdb.Column(pdb.String(100))

	@property
	def password(self):
		raise AttributeError('you sneaky bastard!')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def verify_password(self, password):
		return check_password_hash(
			self.password_hash, password + self.password_salt
		)


class Movie(pdb.Model, UserMixin):
	id    = pdb.Column(pdb.String(128), primary_key=True)
	title = pdb.Column(pdb.String(100))