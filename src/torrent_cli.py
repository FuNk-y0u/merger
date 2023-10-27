from inc import *
from log import *

class TorrentCLI:
	def __init__(self, url: str, username: str, password: str):
		self.qb = Client(url)
		self.qb.login(username, password)

	def get_file_hash(self, file_path: str) -> str:
		try:
			file = open(file_path, "rb")
			metainfo = bencode.bdecode(file.read())
			info = metainfo['info']
			hash = hashlib.sha1(bencode.bencode(info)).hexdigest()
			return hash
		except Exception as e:
			log_error(f"Failed to get hash of file: {file_path}")
			log_error(e)
			return False

	def download_from_file(self, file_path: str, dest: str) -> bool:
		log_info(f"Downloading: {file_path}")
		try:
			file = open(file_path, "rb")
			self.qb.download_from_file(file, savepath = dest)
			return True
		except Exception as e:
			log_error(f"Failed downloading: {file_path}")
			log_error(e)
			return False

	def get_completed_list(self) -> dict:
		completed = {}

		torrents = self.qb.torrents(filter = "completed")
		for torr in torrents:
			completed.update({ torr["hash"]: torr["content_path"] })

		return completed

