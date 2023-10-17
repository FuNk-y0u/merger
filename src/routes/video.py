from src.inc import *
from src.defines import *
from src.model import *

def get_video():
	return send_file(f'database/{request.args.get("id")}.webm')

def get_video_list() -> Response:
	query = Movie.query.all()
	if not query:
		return MResponse(
			FAILED,
			"Database empty.",
			[]
		).as_json()

	videos = {}
	for movie in query:
		videos.update({ movie.id: movie.title })

	return MResponse(
		SUCESS,
		"Videos.",
		[videos]
	).as_json()
