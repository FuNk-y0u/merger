from inc import *

from defines import *
from model import *
from routes.watch import watch, video
from routes.lobby import *
from routes.registration import *

app = Flask(__name__)
CORS(app)

load_dotenv()

# Initializing database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///items.db"
pdb.init_app(app)

# Global app states
app.config[M_LOBBIES] = {}

# Registration endpoints
app.add_url_rule("/signup", view_func=signup, methods=["POST"])
app.add_url_rule("/login", view_func=login, methods=["POST"])

# Lobby endpoints
app.add_url_rule("/lobby_create", view_func=lobby_create, methods=["POST"])
app.add_url_rule("/lobby_add_movie", view_func=lobby_add_movie, methods=["POST"])
app.add_url_rule("/lobby_join", view_func=lobby_join, methods=["POST"])
app.add_url_rule("/lobby_update_host_state", view_func=lobby_update_host_state, methods=["POST"])
app.add_url_rule("/lobby_get_host_state", view_func=lobby_get_host_state, methods=["POST"])
app.add_url_rule("/get_video", view_func=video, methods=["get"])

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8000, debug=True)
