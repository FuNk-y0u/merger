from utils.inc import *
from utils.defines import *
from utils.log import *

from queue_handler import *


# 12 min for a single file

class MergerDB:
	def __init__(
			self,
			app: Flask,
			logger: Logger,
			fps: float
		):
		self.app = app
		self.logger = logger
		self.fps = fps

		self.queue_handler = QueueHandler(self.logger, self.app)

		self.TORR_FILE_PATH  = os.getenv("TORR_FILE_PATH")

		# TORR Dir
		if not os.path.exists(self.TORR_FILE_PATH):
			os.mkdir(self.TORR_FILE_PATH)

		# DB initialization
		with self.app.app_context():
			pdb.init_app(self.app)

	def run(self):
		while True:
			movies = self.__get_unuploaded_movies()
			self.queue_handler.append_movies(movies)
			self.queue_handler.update()
			time.sleep(self.fps)

	def __get_unuploaded_movies(self) -> dict[str, MovieInfo]:
		movies: dict[str, MovieInfo] = {}

		with self.app.app_context():
			query = Movie.query.filter_by(uploaded = False).all()
			for q in query:
				info = MovieInfo(
					id  = q.id,
					url = q.torrent_url,
					hash = None,
					content_path = None,
					status = MovieStatus.QUEUED
				)
				movies.update({ q.id: info })

		return movies

