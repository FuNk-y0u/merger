from utils.inc import *


class Logger:
	def __init__(self):
		self.stream = ""
		self.size = 0

	def sucess(self, msg) -> int:
		return self.__write(f"[SUCESS]:  {msg}\n")

	def info(self, msg) -> int:
		return self.__write(f"[INFO]:    {msg}\n")

	def error(self, msg) -> int:
		return self.__write(f"[ERROR]:   {msg}\n")

	def warn(self, msg) -> int:
		return self.__write(f"[WARNING]: {msg}\n")

	def __write(self, msg) -> int:
		length = len(msg)
		sys.stdout.write(msg)

		self.stream += msg
		self.size += length

		return length

