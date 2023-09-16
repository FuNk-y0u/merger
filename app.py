from inc import *
from routes.watch import watch, video
from routes.record import record

app = Flask(__name__)
CORS(app)

app.add_url_rule("/",view_func=video, methods=["GET"])
app.add_url_rule("/",view_func=watch, methods=["POST"])
app.add_url_rule("/record",view_func=record, methods=["POST"])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)