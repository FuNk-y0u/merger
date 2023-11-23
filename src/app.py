from mergerdb import *


class App:
	def __init__(self):
		load_dotenv()

		#TODO: Implement process_info for cli
		#TODO: Implement cli

		self.app = Flask(__name__)
		CORS(self.app)
		self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")

		self.logger = Logger()
		self.mergerdb = MergerDB(self.app, self.logger, 1)

	def run(self):
		self.mergerdb.run()


if __name__ == "__main__":
	app = App()
	app.run()
