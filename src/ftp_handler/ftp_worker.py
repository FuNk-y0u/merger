from utils.inc     import *
from utils.log     import *
from utils.defines import *

from ftp_handler.ftp_cli import *


class FTP_Worker:
	def __init__(self, id: int, logger: Logger):
		self.id = id
		self.logger = logger
		self.status: WorkerStatus = WorkerStatus.FREE

		self.FTP_UPDATE_TIME = int(os.getenv("FTP_UPDATE_TIME"))

		self.ftp = FTP_CLI(
			self.logger,
			os.getenv("FTP_USER"),
			os.getenv("FTP_PASSWORD"),
			os.getenv("FTP_SERVER")
		)
		self.ftp.login()

		# Total bytes and uploaded bytes
		self.total     = 0
		self.uploaded  = 0

	def upload_movie(
		self,
		movie_info: MovieInfo,
		sucess_callback: Callable[[str], None],
		error_callback: Callable[[str], None]
	) -> None:
		file_path  = self.__change_filename(movie_info.id, movie_info.content_path)
		self.total = os.path.getsize(file_path)

		res = self.ftp.store_file(
			file_path,
			self.__handle_progress
		)
		if not res:
			self.logger.error(f"id: {movie_info.id} - Failed to upload through ftp")
			error_callback(movie_info.id)
			return

		self.status = WorkerStatus.HALT
		time.sleep(self.FTP_UPDATE_TIME)

		self.total     = 0
		self.uploaded  = 0
		self.status = WorkerStatus.FREE

		sucess_callback(movie_info.id)

	def __change_filename(self, id: str, content_path: str) -> str:
		# Finding the filename
		contents = os.listdir(content_path)
		file_name = ""
		for file in contents:
			if file.endswith(".mp4"): file_name = file

		if not file_name: return None

		# Changing the filename
		file_path = f"{content_path}/{file_name}"
		new_path  = f"{content_path}/{id}.mp4"

		os.rename(file_path, new_path)
		return new_path

	def __handle_progress(self, sent: bytes) -> None:
		self.uploaded += len(sent)

