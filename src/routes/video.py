from src.inc import *
from src.defines import *
from src.model import *
from src.utils import *

def get_video() -> Response:
	payload = request.get_json()

	if not verify_key(["video_id"], payload):
		return MResponse(
			FAILED,
			"`id` are the required payload fields.",
			[]
		).as_json()

	id = payload["video_id"]

	movie = Movie.query.filter_by(id = id).first()
	if not movie :
		return MResponse(
			FAILED,
			f"Invalid video id: {id}",
			[]
		).as_json()

	if not movie.uploaded:
		return MResponse(
			FAILED,
			f"Movie {id} hasnt been uploaded yet.",
			[]
		).as_json()

	return MResponse(
		SUCESS,
		f"Sucessfully fetched vide url.",
		[{
			"url": movie.video_url,
			"subtitle": movie.subtitle_url
		}]
	).as_json()


def get_video_list() -> Response:
	payload = request.get_json()

	if not verify_key(["uploaded", "page_no", "per_page"], payload):
		return MResponse(
			FAILED,
			"`uploaded`, `page_no`, `per_page` are the required payload fields.",
			[]
		).as_json()

	uploaded = payload["uploaded"]
	page_no  = payload["page_no"]
	per_page = payload["per_page"]

	try:
		query = Movie.query.filter_by(uploaded=uploaded).paginate(page=page_no, per_page=per_page)
	except Exception as e:
		return MResponse(
			FAILED,
			e,
			[]
		).as_json()

	if not query:
		return MResponse(
			FAILED,
			"Reached empty page",
			[]
		).as_json()

	videos = {}
	for movie in query:
		videos.update({
			movie.id: {
				"title": movie.title,
				"description": movie.description,
				"poster_url": movie.poster_url,
				"video_url": movie.video_url
			}
		})

	return MResponse(
		SUCESS,
		"Videos.",
		[videos]
	).as_json()

def get_video_metadata() -> Response:
	payload = request.get_json()

	if not verify_key(["video_id"], payload):
		return MResponse(
			FAILED,
			"`id` are the required payload fields.",
			[]
		).as_json()

	id = payload["video_id"]

	movie = Movie.query.filter_by(id = id).first()
	if not movie :
		return MResponse(
			FAILED,
			f"Invalid video id: {id}",
			[]
		).as_json()

	if not movie.uploaded:
		return MResponse(
			FAILED,
			f"Movie {id} hasnt been uploaded yet.",
			[]
		).as_json()

	return MResponse(
		SUCESS,
		f"Sucessfully fetched vide url.",
		[{
			"title": movie.title,
			"description": movie.description,
			"poster_url": movie.poster_url
		}]
	).as_json()