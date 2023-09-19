from inc import *
from defines import *
from utils import verify_key

def auth_token(func):
	@wraps(func)	

	def decorated(*args, **kwargs):
		payload = request.get_json()

		if not verify_key(["token"], payload):
			return MResponse(
				FAILED,
				"`token` is the required payload fields.",
				[]
			).as_json()

		token = payload['token']
		if not token:
			return MResponse(FAILED, "`token` is empty.", []).as_json()

		try:
			jwt.decode(
				token,
				os.getenv('SECRET_KEY'),
				algorithms=['HS256']
			)
			return func(*args, **kwargs)
		except jwt.exceptions.ExpiredSignatureError as e:
			return MResponse(TOKEN_EXIPRED, "Token has been expired.", []).as_json()
		except Exception as e:
			return MResponse(FAILED, "Token is invalid", []).as_json()

	return decorated
