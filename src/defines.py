from src.inc import *


# Status codes
SUCESS        = 200
FAILED        = 400
TOKEN_EXIPRED = 401
NO_ADMIN      = 402
NOT_FOUND     = 404


# Labels
M_LOBBIES = "M_LOBBIES"


@dataclasses.dataclass
class HostState:
	host_time: float
	paused: bool
	playing: bool
	speed: float

	def as_dict(self) -> dict:
		return self.__dict__

	def as_json(self) -> Response:
		return jsonify(
			dataclasses.asdict(self)
		)

class Lobby:
	def __init__(self, admin_id: str):
		self.id = str(uuid.uuid4())
		self.admins = [admin_id]
		self.members = [admin_id]
		self.movie_id = None
		self.host_state = None

	def as_dict(self) -> dict:
		return self.__dict__


@dataclasses.dataclass
class MResponse:
	status: int
	log: str
	ext: list

	def as_json(self) -> Response:
		return jsonify(
			dataclasses.asdict(self)
		)
