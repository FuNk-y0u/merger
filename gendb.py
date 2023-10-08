from app import *

import sys
import shutil


def add_movie(path: str, title: str):
	# Checking if movie already exists
	query = Movie.query.filter_by(title=title).first()
	if query:
		return

	# Creating new movie object
	id = str(uuid.uuid4())
	new_movie = Movie(
		id=id,
		title=title
	)
	pdb.session.add(new_movie)
	pdb.session.commit()

	shutil.copy2(path, f"instance/videos/{id}.webm");
	print(f"Sucessfully copied `{title}` to the database.")

with app.app_context():
	pdb.create_all()

	# Create movies directory
	if not os.path.exists("instance/videos"):
		os.mkdir("instance/videos")


	add_movie("static/videos/sad_edit.webm", "sad_edit")
	add_movie("static/videos/to_be_continued.webm", "to_be_continued")
	add_movie("static/videos/101.webm", "type")

	sys.exit(0)
