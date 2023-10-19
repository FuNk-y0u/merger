from src.inc import *
from src.model import *
from src.defines import *
from src.utils import verify_key
from src.routes.auth import auth_token

from src.mergerdb.scrapper import *

class MergerDB:
	def __init__(self, app: Flask):
		with app.app_context():
			pdb.init_app(app)
			pdb.create_all()

		self.scrapper = Scrapper()

	@auth_token
	def search_new_movie(self) -> Response:
		payload = request.get_json()

		if not verify_key(["movie_name"], payload):
			return MResponse(
				FAILED,
				"`movie_name` are the required payload fields.",
				[]
			).as_json()

		movies = self.scrapper.scrape(payload["movie_name"])
		return MResponse(
			SUCESS,
			f"Found {len(movies)} movies",
			[movies]
		).as_json()

	@auth_token
	def add_new_movie(self) -> Response:
		payload = request.get_json()

		if not verify_key(["title", "poster_url", "torrent_url"], payload):
			return MResponse(
				FAILED,
				"`title`, `poster_url`, `torrent_url` are the required payload fields.",
				[]
			).as_json()

		# Checking if movie already exists
		query = Movie.query.filter_by(title=payload["title"]).first()
		if query:
			return MResponse(
				FAILED,
				f"Movie `{payload['title']}` is already available.",
				[]
			).as_json()

		# Creating new movie object
		id = str(uuid.uuid4())
		new_movie = Movie(
			id          = id,
			title       = payload["title"],
			poster_url  = payload["poster_url"],
			torrent_url = payload["torrent_url"],
			uploaded    = False
		)

		pdb.session.add(new_movie)
		pdb.session.commit()

		return MResponse(
			SUCESS,
			f"Sucessfully added `{payload['title']}` to `comming soon` list",
			[]
		).as_json()

