from model import *
from app import *

import sys

with app.app_context():
	pdb.create_all()
	sys.exit(0)