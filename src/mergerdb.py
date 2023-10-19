from inc import *
from log import *
from defines import *

from torrent_cli import TorrentCLI
from scrapper    import Scrapper


class MergerDB:
	def __init__(self, app: Flask):
		self.app = app
		self.torr_cli = TorrentCLI(
			os.getenv("TORRENT_DEV_URL"),
			os.getenv("TORRENT_USERNAME"),
			os.getenv("TORRENT_PASSWORD")
		)

		self.scrapper = Scrapper(
			os.getenv("FILEMOON_USERNAME"),
			os.getenv("FILEMOON_PASSWORD")
		)

		with self.app.app_context():
			pdb.init_app(self.app)

		self.movie_queue: dict[str, MovieInfo] = {}
		self.running = True

		self.MAX_TORR_POOL      = int(os.getenv("MAX_TORR_POOL"))
		self.TORR_FILE_PATH     = os.getenv("TORR_FILE_PATH")

		# TORR Dir
		if not os.path.exists(self.TORR_FILE_PATH):
			os.mkdir(self.TORR_FILE_PATH)

	def run(self):
		log_info("Starting queue thread...")
		threading.Thread(target = self.__queue_thread, args=()).start()

		log_info("Starting MergerDB client...")
		while self.running:
			movies = self.__get_unuploaded_movies()
			self.__append_to_movie_queue(movies)
			time.sleep(5 * 60)

	def __get_unuploaded_movies(self) -> dict[str, MovieInfo]:
		movies: dict[str, MovieInfo] = {}

		with self.app.app_context():
			query = Movie.query.filter_by(uploaded = False).all()
			for q in query:
				info = MovieInfo(
					id  = q.id,
					url = q.torrent_url,
					torr_hash = None,
					status = MovieStatus.STALLED
				)
				movies.update({ q.id: info })

		return movies

	def __append_to_movie_queue(self, movies: dict[str, MovieInfo]):
		for movie_id in movies:
			if movie_id not in self.movie_queue:
				self.movie_queue.update({
					movie_id: movies[movie_id]
				})
				log_info(f"Added movie to the queue - id: {movie_id}")

	def __download_torr_file(self, file_path: str, torrent_url: str) -> str:
		log_info(f"Downloading TORR: {file_path}")
		torr_file = requests.get(torrent_url, allow_redirects = True)

		open(file_path, "wb").write(torr_file.content)
		return self.torr_cli.get_file_hash(file_path)

	def __handle_completed_movie(self, movie_info: MovieInfo, movie_path: str):
		log_sucess(f"Downloaded movie - id: {movie_info.id} at '{movie_path}'")

		# Deleting torr file
		torr_file = f"{self.TORR_FILE_PATH}/{movie_info.id}.torrent"
		os.remove(torr_file)

		# Remove from queue
		self.movie_queue.pop(movie_info.id)

		# TODO: Call to FTP client

	def __handle_stalled_movie(self, movie_info: MovieInfo):
		file_path = f"{self.TORR_FILE_PATH}/{movie_info.id}.torrent"

		movie_info.torr_hash = self.__download_torr_file(
			file_path,
			movie_info.url
		)
		self.torr_cli.download_from_file(file_path)

		movie_info.status = MovieStatus.DOWNLOADING

	def __handle_downloading_movie(self, movie_info: MovieInfo):
		completed = self.torr_cli.get_completed_list()

		if not movie_info.torr_hash: return

		if movie_info.torr_hash in completed:
			movie_info.status = MovieStatus.COMPLETED
			self.__handle_completed_movie(
				movie_info,
				completed[movie_info.torr_hash]
			)

	def __queue_thread(self):
		while self.running:
			# NOTE: Getting 5 movies at a time
			movie_ids = list(self.movie_queue.keys())[:self.MAX_TORR_POOL]

			for movie_id in movie_ids:
				movie_info = self.movie_queue[movie_id]

				if movie_info.status == MovieStatus.STALLED:
					self.__handle_stalled_movie(movie_info)
				elif movie_info.status == MovieStatus.DOWNLOADING:
					self.__handle_downloading_movie(movie_info)

			# time.sleep(5 * 60)
