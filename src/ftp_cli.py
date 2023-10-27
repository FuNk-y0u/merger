from inc import *
from log import *


class FileMoonFTP:
	def __init__(self, user:str, password:str, server:str) -> None:
		self.extenstions = [".mp4",".mkv",".avi",".webm",".ts",".mpg",".mpeg",".vob",".flv",".wmv",".3gp",".mov"]
		self.user = user
		self.password = password
		self.server = server
		self.ftp = None

	def login(self):
		self.ftp = FTP()
		log_info(f"Connecting to fpt server: {self.server}")

		try:
			self.ftp.connect(self.server)
			log_info(f"Loggin in as account: {self.user}")
			self.ftp.login(self.user, self.password)
			log_sucess(f"Sucessfully logged into account: {self.user}")

		except Exception as e:
			log_error("Unexpected error occured during login.. ")
			log_error(e)
	
	def store_file(self, filePath:str) -> bool:

		if not os.path.exists(filePath):
			log_error(f"The file {filePath} doesnot exists.. ")
			return False
		
		filename = os.path.basename(filePath)
		filesize = os.path.getsize(filePath)

		is_valid = False

		for extension in self.extenstions:

			if filename.endswith(extension):
				is_valid = True
				with tqdm(unit = 'blocks', unit_scale = True, leave = False, miniters = 1, desc = f'Uploading {filename}', total = filesize) as tqdm_instance:
					try:
						self.ftp.storbinary("STOR " + filename, open(filePath,"rb"), callback= lambda sent: tqdm_instance.update(len(sent)))
					except Exception as e:
						log_error("Network Error Encountered")
						log_error(e)
						return False

				return True
			else:
				pass

		if is_valid == False:
			log_error("Your file extension is not allowed! Allowed extensions are: ")
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
