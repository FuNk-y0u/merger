from inc import *
from mergerdb import *

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initializing database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DEV_DB_URL")
mergerdb = MergerDB(app)
mergerdb.run()
