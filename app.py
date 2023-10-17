from src.inc import *

from src.defines import *
from src.model import *
from src.routes.video import *
from src.routes.lobby import *
from src.routes.registration import *
from src.routes.auth import *

app = Flask(__name__)
CORS(app)

load_dotenv()

# Initializing database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
pdb.init_app(app)

# Global app states
app.config[M_LOBBIES] = {}

# Registration endpoints
app.add_url_rule("/auth", view_func=auth, methods=["POST"])
app.add_url_rule("/signup", view_func=signup, methods=["POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])

# Lobby endpoints
app.add_url_rule("/lobby_create", view_func=lobby_create, methods=["POST"])
app.add_url_rule("/lobby_add_movie", view_func=lobby_add_movie, methods=["POST"])
app.add_url_rule("/lobby_join", view_func=lobby_join, methods=["POST"])
app.add_url_rule("/lobby_leave", view_func=lobby_leave, methods=["POST"])
app.add_url_rule("/lobby_update_host_state", view_func=lobby_update_host_state, methods=["POST"])
app.add_url_rule("/lobby_get_host_state", view_func=lobby_get_host_state, methods=["POST"])
app.add_url_rule("/lobby_get", view_func=lobby_get, methods=["POST"])

app.add_url_rule("/get_video", view_func=get_video, methods=["GET"])
app.add_url_rule("/get_video_list", view_func=get_video_list, methods=["GET"])

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)
