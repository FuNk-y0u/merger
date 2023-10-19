from inc import *
from torrent_cli import TorrentCLI
from log import *

pdb = SQLAlchemy()

class Movie(pdb.Model, UserMixin):
	id          = pdb.Column(pdb.String(128), primary_key=True)
	title       = pdb.Column(pdb.String())
	poster_url  = pdb.Column(pdb.String())
	torrent_url = pdb.Column(pdb.String())
	video_url   = pdb.Column(pdb.String())
	uploaded    = pdb.Column(pdb.Boolean, default = False)

	def as_dict(self) -> dict:
		d = self.__dict__
		d.pop("_sa_instance_state")
		return d


class MovieStatus:
	STALLED     = 0
	DOWNLOADING = 1
	COMPLETED   = 2


@dataclasses.dataclass
class MovieInfo:
	id : str
	url: str
	torr_hash: str
	status: MovieStatus


class MergerDB:
	def __init__(self, app: Flask):
		self.app = app
		self.torr_cli = TorrentCLI(
			os.getenv("TORRENT_DEV_URL"),
			os.getenv("TORRENT_USERNAME"),
			os.getenv("TORRENT_PASSWORD")
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
		threading.Thread(target = self.queue_thread, args=()).start()

		log_info("Starting progress thread...")
		threading.Thread(target = self.progress_thread, args=()).start()

		log_info("Starting MergerDB client...")
		while self.running:
			movies = self.__get_unuploaded_movies()
			self.__append_to_movie_queue(movies)
			time.sleep(5 * 60)

	def queue_thread(self):
		while self.running:
			# NOTE: Getting 5 movies at a time
			movie_ids = list(self.movie_queue.keys())[:self.MAX_TORR_POOL]

			for movie_id in movie_ids:
				movie_info = self.movie_queue[movie_id]

				# Downloading
				if movie_info.status == MovieStatus.STALLED:
					file_path = f"{self.TORR_FILE_PATH}/{movie_id}.torrent"

					movie_info.torr_hash = self.__download_torr_file(
						file_path,
						movie_info.url
					)
					self.torr_cli.download_from_file(file_path)

					movie_info.status = MovieStatus.DOWNLOADING

			# time.sleep(5 * 60)

	def progress_thread(self):
		while self.running:
			# NOTE: Getting 5 movies at a time
			movie_ids = list(self.movie_queue.keys())[:self.MAX_TORR_POOL]

			for movie_id in movie_ids:
				movie_info = self.movie_queue[movie_id]

				if movie_info.status == MovieStatus.DOWNLOADING:
					completed = self.torr_cli.get_completed_list()

					if not movie_info.torr_hash: continue

					if movie_info.torr_hash in completed:
						movie_info.status = MovieStatus.COMPLETED
						self.__handle_completed_movies(movie_info)

			# time.sleep(5 * 60)

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

	def __handle_completed_movies(self, movie_info: MovieInfo):
		log_sucess(f"Downloaded movie - id: {movie_info.id}")

		# Deleting torr file
		torr_file = f"{self.TORR_FILE_PATH}/{movie_info.id}.torrent"
		os.remove(torr_file)

		# Remove from queue
		self.movie_queue.pop(movie_info.id)

		# TODO: Call to FTP client
