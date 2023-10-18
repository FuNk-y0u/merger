from src.inc import *

class TorrentCLI:
	def __init__(self, url: str, username: str, password: str):
		self.qb = Client(url)
		self.qb.login(username, password)

	def get_file_hash(self, file_path: str) -> str:
		torrent_file = open(file_path, "rb")
		metainfo = bencode.bdecode(torrent_file.read())
		info = metainfo['info']
		hash = hashlib.sha1(bencode.bencode(info)).hexdigest()
		return hash

	def progress_tracker(self):
		#TODO: Do a progress tracker
		torrents = self.qb.torrents(filter="downloading")
		hash = self.get_file_hash(file_path)
		for torrent in torrents:
			if torrent["hash"] == hash:
				print(json.dumps(torrent, indent=4))

	def download_from_file(self, file_path: str):
		file = open(file_path, "rb")
		self.qb.download_from_file(file)

