from inc import *

pdb = SQLAlchemy()


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
