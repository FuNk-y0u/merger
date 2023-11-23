from utils.inc import *
from utils.log import *

from ftp_handler.ftp_cli    import *
from ftp_handler.ftp_worker import *


class FTP_Handler:
	def __init__(self, logger: Logger):
		self.logger = logger
		self.MAX_FTP_POOL = int(os.getenv("MAX_FTP_POOL"))

		self.ftp_workers: list[FTP_Worker] = [
			FTP_Worker(
				i,
				self.logger
			) for i in range(self.MAX_FTP_POOL)
		]

	def get_free_worker(self) -> FTP_Worker | None:
		for worker in self.ftp_workers:
			if worker.status == WorkerStatus.FREE:
				return worker
		return None

	def update(
		self,
		queue: dict[str, MovieInfo],
		sucess_callback: Callable[[str], None],
		error_callback: Callable[[int, str], None]
	) -> None:
		worker = self.get_free_worker()
		if not worker: return

		# Running the loop only once cuz a worker only handles a single movie
		for movie_id in queue:
			movie_info = queue[movie_id]

			if movie_info.status == MovieStatus.FTP_QUEUED:
				continue
			movie_info.status = MovieStatus.FTP_QUEUED

			threading.Thread(
				target = worker.upload_movie,
				args = (
					movie_info,
					sucess_callback,
					error_callback
				),
			).start()
			return


