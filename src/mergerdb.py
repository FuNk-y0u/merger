from inc import *
from log import *
from defines import *

from torrent_cli import TorrentCLI
from scrapper    import Scrapper
from ftp_cli     import FileMoonFTP


class MergerDB:
	def __init__(self, app: Flask):
		self.app = app
		self.torr_cli = TorrentCLI(
			os.getenv("TORRENT_URL"),
			os.getenv("TORRENT_USERNAME"),
			os.getenv("TORRENT_PASSWORD")
		)

		self.scrapper = Scrapper(
			os.getenv("FILEMOON_USERNAME"),
			os.getenv("FILEMOON_PASSWORD")
		)

		self.fftp = FileMoonFTP(
			os.getenv("FTP_USER"),
			os.getenv("FTP_PASSWORD"),
			os.getenv("FTP_SERVER")
		)
		self.fftp.login()

		self.MAX_TORR_POOL   = int(os.getenv("MAX_TORR_POOL"))
		self.DB_UPDATE_TIME  = int(os.getenv("DB_UPDATE_TIME"))
		self.FTP_UPDATE_TIME = int(os.getenv("FTP_UPDATE_TIME"))
		self.TORR_FILE_PATH  = os.getenv("TORR_FILE_PATH")

		self.movie_queue: dict[str, MovieInfo] = {}
		self.running = True

		# TORR Dir
		if not os.path.exists(self.TORR_FILE_PATH):
			os.mkdir(self.TORR_FILE_PATH)

		# DB initialization
		with self.app.app_context():
			pdb.init_app(self.app)

	def run(self):
		log_info("Starting queue thread...")
		threading.Thread(target = self.__queue_thread, args=()).start()

		log_info("Starting MergerDB client...")
		while self.running:
			movies = self.__get_unuploaded_movies()
			self.__append_to_movie_queue(movies)
			time.sleep(self.DB_UPDATE_TIME)

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
		log_info(f"Downloading TORR: {file_path} from: {torrent_url}")
		torr_file = requests.get(torrent_url, allow_redirects = True)

		open(file_path, "wb").write(torr_file.content)
		return self.torr_cli.get_file_hash(file_path)

	def __handle_completed_movie(self, movie_info: MovieInfo, movie_path: str):
		log_sucess(f"Downloaded movie - id: {movie_info.id} at '{movie_path}'")

		# Deleting torr file
		torr_file = f"{self.TORR_FILE_PATH}/{movie_info.id}.torrent"
		os.remove(torr_file)

		# Finding the filename
		contents = os.listdir(movie_path)
		file_name = ""
		for file in contents:
			if file.endswith(".mp4"): file_name = file

		if not file_name:
			log_error(f"Cannot find the mp4 file for - id: {movie_info.id}")
			return False

		# Changing the filename
		file_path = f"{movie_path}/{file_name}"
		new_path  = f"{movie_path}/{movie_info.id}.mp4"

		os.rename(file_path, new_path)

		# Pusing the movie into filemoon server
		res = self.fftp.store_file(new_path)
		if not res:
			log_error(f"FTP CLI failed to push {movie_path} to cloud.")
			return False

		log_sucess(f"Sucessfully uploaded to filemoon via FTP - id: {movie_info.id}")
		log_info("Waiting for 5 min to fully be available in filemoon...")

		# Wait to fully upload to filemoon
		time.sleep(self.FTP_UPDATE_TIME)

		# Scrapping filemoon for short embeded url
		url = self.scrapper.scrape_url(movie_info.id)
		if not url:
			log_error(f"Cannot find the video url for {movie_info.id}")
			return False

		# Update the database
		log_info(f"Updating database with video url - id: {movie_info.id} & url: {url}")

		with self.app.app_context():
			movie = Movie.query.filter_by(id = movie_info.id).first()
			movie.video_url = url
			movie.uploaded = True

			pdb.session.add(movie)
			pdb.session.commit()

		# Remove from queue
		self.movie_queue.pop(movie_info.id)
		log_sucess(f"Removed - id: {movie_info.id} from queue")

		log_sucess(f"Sucessfully uploaded movie to cloud - id: {movie_info.id}")
		return True

	def __handle_stalled_movie(self, movie_info: MovieInfo) -> bool:
		file_path = f"{self.TORR_FILE_PATH}/{movie_info.id}.torrent"

		hash = self.__download_torr_file(
			file_path,
			movie_info.url
		)
		if not hash: return False

		movie_info.torr_hash = hash

		res = self.torr_cli.download_from_file(file_path, movie_info.id)
		if not res: return False

		movie_info.status = MovieStatus.DOWNLOADING
		return True

	def __handle_downloading_movie(self, movie_info: MovieInfo) -> bool:
		completed = self.torr_cli.get_completed_list()

		if not movie_info.torr_hash: return False

		if movie_info.torr_hash in completed:
			movie_info.status = MovieStatus.COMPLETED
			return self.__handle_completed_movie(
				movie_info,
				completed[movie_info.torr_hash]
			)
		return True

	def __queue_thread(self):
		while self.running:
			movie_ids = list(self.movie_queue.keys())[:self.MAX_TORR_POOL]

			for movie_id in movie_ids:
				movie_info = self.movie_queue[movie_id]

				if movie_info.status == MovieStatus.STALLED:
					res = self.__handle_stalled_movie(movie_info)
					if not res:
						log_error(f"Failed downloading movie - id: {movie_id}")
						self.movie_queue.pop(movie_id)

				elif movie_info.status == MovieStatus.DOWNLOADING:
					res = self.__handle_downloading_movie(movie_info)
					if not res:
						log_error(f"Failed downloading movie - id: {movie_id}")
						self.movie_queue.pop(movie_id)

