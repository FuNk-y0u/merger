from src.inc import *
from src.defines import *
from src.model import *

def get_video():
	return send_file(f'database/{request.args.get("id")}.webm')

def get_video_list() -> Response:
	uploaded = request.args.get("uploaded")
	query = Movie.query.filter_by(uploaded=uploaded).all()

	videos = {}
	for movie in query:
		videos.update({
			movie.id: {
				"title": movie.title,
				"poster_url": movie.poster_url,
				"video_url": movie.video_url
			}
		})

	return MResponse(
		SUCESS,
		"Videos.",
		[videos]
	).as_json()
