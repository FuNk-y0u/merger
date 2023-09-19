from inc import *
from model import pdb, User
from utils import verify_key
from defines import *

def signup() -> Response:
	payload = request.get_json()

	if not verify_key(["email","username","password"], payload):
		return MResponse(
			FAILED,
			"`email`, `username`, `password` are the required payload fields.",
			[]
		).as_json()

	email    = payload["email"]
	username = payload["username"]
	password = payload["password"]

	query = User.query.filter_by(email=email).first()
	if query:
		return MResponse(FAILED, f"email: `{email}` already taken.", []).as_json()

	id = str(uuid.uuid4())
	salt = str(secrets.token_hex(32))
	password += salt

	new_user = User(
		id=id,
		email=email,
		username=username,
		password=password,
		password_salt=salt
	)
	pdb.session.add(new_user);
	pdb.session.commit();

	return MResponse(
		SUCESS,
		f"Sucessfully created account as `{username}`.",
		[]
	).as_json()


def login() -> Response:
	payload = request.get_json()

	if not verify_key(["email", "password"], payload):
		return MResponse(
			FAILED,
			"`email`, `password` are the required payload fields.",
			[]
		).as_json()

	email    = payload["email"]
	password = payload["password"]

	query = User.query.filter_by(email=email).first()
	if not query:
		return MResponse(
			FAILED,
			f"Email: `{email}` doesn`t exists.",
			[]
		).as_json()

	if not query.verify_password(password):
		return MResponse(
			FAILED,
			f"Incorrect password",
			[]
		).as_json()

	#TODO: Check for email verification

	jwt_token = jwt.encode(
		{
			"id": query.id,
			"username": query.username,
			"email": email,
			"exp": datetime.utcnow() + timedelta(days=30)
		},
		os.getenv("SECRET_KEY")
	)

	return MResponse(
		SUCESS,
		f"Sucessfully logged in as `{query.username}`.",
		[{"token": jwt_token}]
	).as_json()
