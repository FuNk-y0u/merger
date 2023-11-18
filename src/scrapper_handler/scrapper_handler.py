from utils.inc     import *
from utils.log     import *
from utils.defines import *

from scrapper_handler.scrapper import *


class ScrapperHandler:
	def __init__(self, logger: Logger, app: Flask):
		self.logger = logger
		self.app = app

		self.scrapper = Scrapper(
			os.getenv("FILEMOON_USERNAME"),
			os.getenv("FILEMOON_PASSWORD")
		)

	def update(
		self,
		queue: dict[str, MovieInfo],
		sucess_callback: Callable[[str], None],
		error_callback: Callable[[str], None]
	) -> None:
		for movie_id in queue:
			movie_info = queue[movie_id]

			if movie_info.status == MovieStatus.SCPR_QUEUED:
				return
			movie_info.status = MovieStatus.SCPR_QUEUED

			url = self.scrapper.scrape_url(movie_info.id)
			if not url:
				self.logger.error(f"id: {movie_info.id} - Failed to scrape url.")
				error_callback(movie_info.id)
				return

			self.__update_db(movie_info.id, url)

			sucess_callback(movie_info.id)

	def __update_db(self, id: str, url: str) -> None:
		with self.app.app_context():
			movie = Movie.query.filter_by(id = id).first()
			movie.video_url = url
			movie.uploaded = True

			pdb.session.add(movie)
			pdb.session.commit()

