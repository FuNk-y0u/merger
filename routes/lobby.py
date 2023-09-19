from inc   import *
from utils import *
from defines import *
from routes.auth import auth_token

from flask import current_app

@auth_token
def lobby_create() -> Response:
	payload = request.get_json()

	if not verify_key(["admin_id"], payload):
		return MResponse(
			FAILED,
			"`admin_id` are the required payload fields.",
			[]
		).as_json()

	admin_id = payload["admin_id"]

	#TODO: Verify admin_id
	new_lobby = Lobby(admin_id)

	current_app.config[M_LOBBIES].update({new_lobby.id: new_lobby})

	return MResponse(
		SUCESS,
		"Sucessfully created lobby",
		[ new_lobby.as_dict() ]
	).as_json()


@auth_token
def lobby_add_movie() -> Response:
	payload = request.get_json()

	if not verify_key(["lobby_id", "movie_id"], payload):
		return MResponse(
			FAILED,
			"`lobby_id`, `movie_id` are the required payload fields.",
			[]
		).as_json()

	lobby_id = payload["lobby_id"]
	movie_id = payload["movie_id"]

	if lobby_id not in current_app.config[M_LOBBIES]:
		return MResponse(
			FAILED,
			"Invalid lobby id.",
			[]
		).as_json()

	#TODO: Handle the case of changing the movie in mid of watching
	lobby = current_app.config[M_LOBBIES][lobby_id]

	#TODO: Verify movie_id
	lobby.movie_id = movie_id

	return MResponse(
		SUCESS,
		"Sucessfully added movie in lobby",
		[ lobby.as_dict() ]
	).as_json()


@auth_token
def lobby_join() -> Response:
	payload = request.get_json()

	if not verify_key(["lobby_id", "user_id"], payload):
		return MResponse(
			FAILED,
			"`lobby_id`, `user_id` are the required payload fields.",
			[]
		).as_json()

	lobby_id = payload["lobby_id"]
	user_id = payload["user_id"]

	if lobby_id not in current_app.config[M_LOBBIES]:
		return MResponse(
			FAILED,
			"Invalid lobby id.",
			[]
		).as_json()

	lobby = current_app.config[M_LOBBIES][lobby_id]

	#TODO: Verify user_id
	lobby.members.append(user_id)

	return MResponse(
		SUCESS,
		"Sucessfully joined lobby",
		[ lobby.as_dict() ]
	).as_json()


@auth_token
def lobby_update_host_state() -> Response:
	payload = request.get_json()

	if not verify_key([
		"lobby_id",
		"host_time",
		"paused",
		"playing",
		"speed"
	], payload):
		return MResponse(
			FAILED,
			"`lobby_id`, `host_time`, `paused`, `playing`, `speed` are the required payload fields.",
			[]
		).as_json()

	lobby_id  = payload["lobby_id"]
	lobby_id  = payload["lobby_id"]
	host_time = payload["host_time"]
	paused    = payload["paused"]
	playing   = payload["playing"]
	speed     = payload["speed"]

	if lobby_id not in current_app.config[M_LOBBIES]:
		return MResponse(
			FAILED,
			"Invalid lobby id.",
			[]
		).as_json()

	lobby = current_app.config[M_LOBBIES][lobby_id]
	lobby.host_state = HostState(
		host_time,
		paused,
		playing,
		speed
	)

	return MResponse(
		SUCESS,
		"Sucessfully added movie in lobby",
		[ lobby.as_dict() ]
	).as_json()


@auth_token
def lobby_get_host_state() -> Response:
	payload = request.get_json()

	if not verify_key(["lobby_id"], payload):
		return MResponse(
			FAILED,
			"`lobby_id` are the required payload fields.",
			[]
		).as_json()

	lobby_id = payload["lobby_id"]
	if lobby_id not in current_app.config[M_LOBBIES]:
		return MResponse(
			FAILED,
			"Invalid lobby id.",
			[]
		).as_json()

	lobby = current_app.config[M_LOBBIES][lobby_id]
	return MResponse(
		SUCESS,
		"Sucessfully fetched host state of lobby",
		[ lobby.host_state.as_dict() ]
	).as_json()
