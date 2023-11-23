from src.inc import *
from src.model import pdb, User
from src.utils import verify_key
from src.defines import *
from src.routes.auth import *
from src.routes.verify_mail import *
from src.template.email_template import *

def signup() -> Response:
	try:
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
	
		# Sending email for verification
		token = jwt.encode({
				'email': email,
				'exp': datetime.utcnow() + timedelta(minutes=30),
			},
			os.getenv('SECRET_KEY')
		)
		sv_url = os.getenv("SV_URL")
		confirm_url = f"{sv_url}/verify_mail/{token}"
		send_mail(email, email_subject, get_email_template(confirm_url))
	
		return MResponse(
			SUCESS,
			f"Check your email for verification.",
			[]
		).as_json()
	except Exception as e:
		return MResponse(
			FAILEd,
			e,
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

	if not query.is_verified:
		return MResponse(
			FAILED,
			f"Email hasn't been verified yet.",
			[]
		).as_json()

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


def connection_check() -> Response:
	return MResponse(
		SUCESS,
		f"server connection sucessfull",
		[{}]
	).as_json()


@auth_token
def get_user() -> Response:
	payload = request.get_json()

	if not verify_key(["id"], payload):
		return MResponse(
			FAILED,
			"`id` are the required payload fields.",
			[]
		).as_json()

	id = payload["id"]
	query = User.query.filter_by(id = id).first()
	if not query:
		return MResponse(
			FAILED,
			"Invalid user id",
			[]
		).as_json()

	user = {
		"email"   : query.email,
		"username": query.username
	}

	return MResponse(
		SUCESS,
		"Sucessfully fetched user data",
		[user]
	).as_json()

