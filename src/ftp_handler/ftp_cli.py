from utils.inc import *
from utils.log import *


class FTP_CLI:
	def __init__(
			self,
			logger: Logger,
			user: str,
			password: str,
			server: str
		):
		self.extenstions = [".mp4",".mkv",".avi",".webm",".ts",".mpg",".mpeg",".vob",".flv",".wmv",".3gp",".mov"]
		self.logger = logger
		self.user = user
		self.password = password
		self.server = server

	def login(self):
		self.ftp = FTP()
		self.logger.info(f"Connecting to fpt server: {self.server}")

		try:
			self.ftp.connect(self.server)
			self.logger.info(f"Loggin in as account: {self.user}")
			self.ftp.login(self.user, self.password)
			self.logger.sucess(f"Sucessfully logged into account: {self.user}")

		except Exception as e:
			self.logger.error("Unexpected error occured during login.. ")
			self.logger.error(e)
	
	def store_file(self, filePath: str, progress_callback: Callable[[bytes], None]) -> bool:
		if not os.path.exists(filePath):
			self.logger.error(f"The file {filePath} doesnot exists.. ")
			return False
		
		filename = os.path.basename(filePath)
		filesize = os.path.getsize(filePath)

		is_valid = False

		for extension in self.extenstions:

			if filename.endswith(extension):
				is_valid = True
				try:
					self.ftp.storbinary("STOR " + filename, open(filePath,"rb"), callback = progress_callback)
				except Exception as e:
					self.logger.error("Network Error Encountered")
					self.logger.error(e)
					return False
				return True
			else:
				pass

		if is_valid == False:
			self.logger.error("Your file extension is not allowed! Allowed extensions are: ")
			for extension in self.extenstions:
				print(extension)
			return False

if __name__ == '__main__':
	load_dotenv()
	username = os.getenv('FTP_USER')
	password = os.getenv('FTP_PASSWORD')
	server = os.getenv('FTP_SERVER')

	fftp = FileMoonFTP(username,password,server)
	fftp.login()
	fftp.store_file('test.mp4')
