from utils.inc import *
from utils.log import *
from utils.defines import *

from state_manager import *
from torrent_handler.torrent_handler import *
from ftp_handler.ftp_handler import *
from scrapper_handler.scrapper_handler import *


class QueueHandler:
	def __init__(self, logger: Logger, app: Flask):
		self.logger = logger

		# Movie queues
		self.movie_queue: dict[str, MovieInfo] = {}
		self.torr_queue : dict[str, MovieInfo] = {}
		self.ftp_queue  : dict[str, MovieInfo] = {}
		self.scpr_queue : dict[str, MovieInfo] = {}

		self.torr_handler = TorrentHandler(logger)
		self.ftp_handler = FTP_Handler(logger)
		self.scpr_handler = ScrapperHandler(logger, app)

	def append_movies(self, movies: dict[str, MovieInfo]):
		for movie_id in movies:
			if movie_id not in self.movie_queue:
				self.movie_queue.update({
					movie_id: movies[movie_id]
				})
				self.torr_queue.update({
					movie_id: movies[movie_id]
				})
				self.logger.info(f"Added movie to the queue - id: {movie_id}")

		state_manager.update_queue(
			QueueType.GLOBAL,
			list(self.movie_queue.keys())
		)
		state_manager.update_queue(
			QueueType.TORR,
			list(self.torr_queue.keys())
		)

	def update(self):
		self.torr_handler.update(
			self.torr_queue.copy(),
			self.__torr_sucess_callback,
			self.__torr_error_callback
		)
		self.ftp_handler.update(
			self.ftp_queue.copy(),
			self.__ftp_sucess_callback,
			self.__ftp_error_callback
		)
		self.scpr_handler.update(
			self.scpr_queue.copy(),
			self.__scpr_sucess_callback,
			self.__scpr_error_callback
		)


	"""
	* Torrent client callback functions
	"""

	def __torr_sucess_callback(self, movie_id: str, content_path: str) -> None:
		movie_info = self.movie_queue[movie_id]
		movie_info.content_path = content_path

		self.torr_queue.pop(movie_id)
		self.ftp_queue.update({ movie_id: movie_info })

		state_manager.update_queue(
			QueueType.TORR,
			list(self.torr_queue.keys())
		)
		state_manager.update_queue(
			QueueType.FTP,
			list(self.ftp_queue.keys())
		)

	def __torr_error_callback(self, movie_id: str) -> None:
		self.torr_queue.pop(movie_id)
		self.movie_queue.pop(movie_id)
		self.logger.error(f"[TORR]({self.worker_id}) -- id: {movie_id} - Failed torrent install, removed from the queue")

		state_manager.update_queue(
			QueueType.GLOBAL,
			list(self.movie_queue.keys())
		)
		state_manager.update_queue(
			QueueType.TORR,
			list(self.torr_queue.keys())
		)


	"""
	* FTP client callback functions
	"""

	def __ftp_sucess_callback(self, movie_id: str) -> None:
		self.ftp_queue.pop(movie_id)
		self.scpr_queue.update({ movie_id: self.movie_queue[movie_id] })

		state_manager.update_queue(
			QueueType.FTP,
			list(self.ftp_queue.keys())
		)
		state_manager.update_queue(
			QueueType.SCPR,
			list(self.scpr_queue.keys())
		)

	def __ftp_error_callback(self, worker_id: int, movie_id: str) -> None:
		self.ftp_queue.pop(movie_id)
		self.movie_queue.pop(movie_id)
		self.logger.error(f"[FTP]({self.worker_id}) -- id: {movie_id} - Failed ftp upload, removed from the queue")

		state_manager.update_queue(
			QueueType.GLOBAL,
			list(self.movie_queue.keys())
		)
		state_manager.update_queue(
			QueueType.FTP,
			list(self.ftp_queue.keys())
		)


	"""
	* Scrapper client callback functions
	"""

	def __scpr_sucess_callback(self, movie_id: str) -> None:
		self.scpr_queue.pop(movie_id)
		self.movie_queue.pop(movie_id)
		self.logger.sucess(f"id: {movie_id} - Sucessfully downloaded movie.")

		state_manager.update_queue(
			QueueType.GLOBAL,
			list(self.movie_queue.keys())
		)
		state_manager.update_queue(
			QueueType.SCPR,
			list(self.scpr_queue.keys())
		)

	def __scpr_error_callback(self, movie_id: str) -> None:
		self.scpr_queue.pop(movie_id)
		self.movie_queue.pop(movie_id)
		self.logger.error(f"id: {movie_id} - Scrapping failed.")

		state_manager.update_queue(
			QueueType.GLOBAL,
			list(self.movie_queue.keys())
		)
		state_manager.update_queue(
			QueueType.SCPR,
			list(self.scpr_queue.keys())
		)
