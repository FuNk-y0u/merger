from src.inc import *

from src.defines import *
from src.model import *

from src.routes.video import *
from src.routes.lobby import *
from src.routes.registration import *
from src.routes.verify_mail  import *
from src.routes.auth import *

from src.mergerdb.mergerdb import *

app = Flask(__name__)
CORS(app)

load_dotenv()

# Initializing database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
mergerdb = MergerDB(app)

# Global app states
app.config[M_LOBBIES] = {}

# Server connection check endpoint
app.add_url_rule("/connect", view_func = connection_check, methods = ["GET"])

# Registration endpoints
app.add_url_rule("/auth",                view_func = auth,        methods = ["POST"])
app.add_url_rule("/signup",              view_func = signup,      methods = ["POST"])
app.add_url_rule("/login",               view_func = login,       methods = ["POST"])
app.add_url_rule("/get_user",            view_func = get_user,    methods = ["POST"])
app.add_url_rule("/verify_mail/<token>", view_func = verify_mail, methods = ["GET"])

# Lobby endpoints
app.add_url_rule("/lobby_create",            view_func = lobby_create,            methods = ["POST"])
app.add_url_rule("/lobby_add_movie",         view_func = lobby_add_movie,         methods = ["POST"])
app.add_url_rule("/lobby_join",              view_func = lobby_join,              methods = ["POST"])
app.add_url_rule("/lobby_leave",             view_func = lobby_leave,             methods = ["POST"])
app.add_url_rule("/lobby_update_host_state", view_func = lobby_update_host_state, methods = ["POST"])
app.add_url_rule("/lobby_get_host_state",    view_func = lobby_get_host_state,    methods = ["POST"])
app.add_url_rule("/lobby_get",               view_func = lobby_get,               methods = ["POST"])
app.add_url_rule("/lobby_get_members",       view_func = lobby_get_members,       methods = ["POST"])

# Video system
app.add_url_rule("/get_video",      view_func = get_video,      methods = ["POST"])
app.add_url_rule("/get_video_list", view_func = get_video_list, methods = ["POST"])
app.add_url_rule("/search_video", view_func = search_video, methods = ["POST"])
app.add_url_rule("/get_video_metadata", view_func = get_video_metadata, methods = ["POST"])

# Database system
app.add_url_rule("/search_new_movie", view_func = mergerdb.search_new_movie, methods = ["POST"])
app.add_url_rule("/add_new_movie",    view_func = mergerdb.add_new_movie,    methods = ["POST"])

if __name__ == "__main__":
  app.run(host = "127.0.0.1", port = os.getenv("PORT"), debug = True)
