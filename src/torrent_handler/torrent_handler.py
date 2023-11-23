from utils.inc import *
from utils.log import *

from torrent_handler.torrent_cli    import *
from torrent_handler.torrent_worker import *


class TorrentHandler:
	def __init__(self, logger: Logger):
		self.logger = logger
		self.MAX_TORR_POOL = int(os.getenv("MAX_TORR_POOL"))

		self.torr_cli = TorrentCLI(
			self.logger,
			os.getenv("TORRENT_URL"),
			os.getenv("TORRENT_USERNAME"),
			os.getenv("TORRENT_PASSWORD")
		)

		self.torr_workers: list[TorrentWorker] = [
			TorrentWorker(
				i,
				self.logger,
				self.torr_cli
			) for i in range(self.MAX_TORR_POOL)
		]

	def get_free_worker(self) -> TorrentWorker | None:
		for worker in self.torr_workers:
			if worker.status == WorkerStatus.FREE:
				return worker
		return None

	def update(
		self,
		queue: dict[str, MovieInfo],
		sucess_callback: Callable[[str, str], None],
		error_callback: Callable[[int, str], None]
	) -> None:
		worker = self.get_free_worker()
		if not worker: return

		# Running the loop only once cuz a worker only handles a single movie
		for movie_id in queue:
			movie_info = queue[movie_id]

			if movie_info.status == MovieStatus.TORR_QUEUED:
				continue
			movie_info.status = MovieStatus.TORR_QUEUED

			threading.Thread(
				target = worker.download_movie,
				args = (
					movie_info,
					sucess_callback,
					error_callback
				),
			).start()
			return

