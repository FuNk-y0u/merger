from utils.inc import *

PROCESS_FILE = "process_info.json"

pdb = SQLAlchemy()


class MovieStatus:
	QUEUED      = "QUEUED"
	TORR_QUEUED = "TORR_QUEUED"
	FTP_QUEUED  = "FTP_QUEUED"
	SCPR_QUEUED = "SCPR_QUEUED"

class WorkerStatus:
	OCCUPIED = "OCCUPIED"
	HALT     = "HALT"
	FREE     = "FREE"


@dataclasses.dataclass
class MovieInfo:
	id : str
	url: str
	hash: str
	content_path: str
	status: MovieStatus


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
