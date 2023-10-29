import {
	server_ip,
	server_query,
	response_status,
	redirect_page,
} from "./../../utils/utils.js";


/*
 * Queries backend to join the lobby
 */

const join_lobby = async (lobby_id) => {
	let payload = {
		token   : localStorage.getItem("token"),
		lobby_id: lobby_id,
		user_id : localStorage.getItem("user_id")
	};

	let response = await server_query("/lobby_join", "POST", payload);
	if (response.status != response_status.SUCESS) {
		return [null, response.log];
	}

	let lobby = response.ext[0];
	return [lobby, response.log];
}


/*
 * Querying backend to create a lobby.
 */

const create_lobby = async (movie_id) => {
	let payload = {
		token: localStorage.getItem("token"),
		admin_id: localStorage.getItem("user_id")
	};

	let response = await server_query("/lobby_create", "POST", payload);
	if (response.status != response_status.SUCESS) {
		return [null, response.log];
	}

	let lobby = response.ext[0];

	// Adding movie
	payload = {
		token: localStorage.getItem("token"),
		lobby_id: lobby.id,
		movie_id: movie_id
	};

	response = await server_query("/lobby_add_movie", "POST", payload);
	if (response.status == response_status.FAILED) {
		return [null, response.log];
	}

	lobby = response.ext[0];
	return [lobby, response.log];
}

export {
	join_lobby,
	create_lobby
}
