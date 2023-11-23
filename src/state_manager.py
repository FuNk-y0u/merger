from utils.log import *
from utils.defines import *
from utils.inc import *


class QueueType:
	GLOBAL = "global"
	TORR   = "torr"
	FTP    = "ftp"
	SCPR   = "scpr"


class StateManager:
	def __init__(self):
		self.state = {
			"queue": {
				QueueType.GLOBAL: [],
				QueueType.TORR  : [],
				QueueType.FTP   : [],
				QueueType.SCPR  : []
			},

			"torr_workers": {},
			"ftp_workers": {}
		}

	def save(self) -> None:
		obj = json.dumps(self.state, indent = 2)
		with open(STATE_FILE, "w") as f:
			f.write(obj)

	def update_queue(self, qt: QueueType, queue: list[str]) -> None:
		self.state["queue"].update({ qt: queue })
		self.save()

	def update_torr_worker(self, id: int, status: WorkerStatus) -> None:
		self.state["torr_workers"].update({
			id: {
				"status": status
			}
		})
		self.save()

	def update_ftp_worker(self, id: int, status: WorkerStatus, progress: float) -> None:
		self.state["ftp_workers"].update({
			id: {
				"status"  : status,
				"progress": progress
			}
		})
		self.save()


# Creating a global state manager
state_manager = StateManager()
