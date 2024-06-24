from utils.inc     import *
from utils.log     import *
from utils.defines import *

from state_manager import *
from torrent_handler.torrent_cli import *


class TorrentWorker:
	def __init__(self, id: int, logger: Logger, torr_cli: TorrentCLI):
		self.id       = id
		self.logger   = logger
		self.torr_cli = torr_cli
		self.status: WorkerStatus = WorkerStatus.FREE

		self.TORR_FILE_PATH  = os.getenv("TORR_FILE_PATH")

		self.update_state()

	def update_state(self) -> None:
		state_manager.update_torr_worker(self.id, self.status)

	def download_movie(
		self,
		movie_info: MovieInfo,
		sucess_callback: Callable[[str, str], None],
		error_callback: Callable[[int, str], None]
	) -> None:
		self.status = WorkerStatus.OCCUPIED

		self.update_state()

		if not self.__download_torr(movie_info):
			self.status = WorkerStatus.FREE
			self.update_state()
			error_callback(self.id, movie_info.id)
			return

		content_path = self.__wait_for_completion(movie_info)

		self.status = WorkerStatus.FREE
		self.update_state()

		self.__cleanup(movie_info)

		sucess_callback(movie_info.id, content_path)

	def __download_torr_file(self, file_path: str, torrent_url: str) -> str:
		self.logger.info(f"[TORR]({self.id}) -- Downloading TORR: {file_path} from: {torrent_url}")
		torr_file = requests.get(torrent_url, allow_redirects = True)

		open(file_path, "wb").write(torr_file.content)
		return self.torr_cli.get_file_hash(file_path)

	def __download_torr(self, movie_info: MovieInfo) -> bool:
		file_path = f"{self.TORR_FILE_PATH}/{movie_info.id}.torrent"

		movie_info.hash = self.__download_torr_file(
			file_path,
			movie_info.url
		)
		if not movie_info.hash: return False

		return self.torr_cli.download_from_file(file_path, movie_info.id)

	def __cleanup(self, movie_info: MovieInfo) -> None:
		self.torr_cli.remove_torr(movie_info.hash)

		file_path = f"{self.TORR_FILE_PATH}/{movie_info.id}.torrent"
		os.remove(file_path)

	"""
	Queries the list of completed movies and checks if the current movie
	has been completed downloading.
	"""

	def __wait_for_completion(self, movie_info: MovieInfo) -> str:
		comp_list = self.torr_cli.get_completed_list()
		while movie_info.hash not in comp_list:
			comp_list = self.torr_cli.get_completed_list()

		return comp_list[movie_info.hash]
