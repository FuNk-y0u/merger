from inc import *
from model import *
from app import *

import sys

# Create movies directory
if not os.path.exists("database"):
	os.mkdir("database")


def add_movie(path: str, title: str):
	id = str(uuid.uuid4())
	new_movie = Movie(
		id=id,
		title=title
	)
	pdb.session.add(new_movie)
	pdb.session.commit()

	os.system(f"copy {path} database\\{id}.webm")
	print(f"Sucessfully copied `{title}` to the database.")

with app.app_context():
	pdb.create_all()

	add_movie("static\\videos\\video.webm", "video")

	sys.exit(0)