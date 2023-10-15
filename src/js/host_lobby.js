import {
	server_ip,
	server_query,
	response_status,
	redirect
} from "./util.js";
import { Modal } from "./modal.js"

const url_params = new URLSearchParams(window.location.search);
const video = document.getElementById("player");

const modal_root = document.getElementById("modal_root");
const modal = new Modal(modal_root);

/*
 * Return button
 */

const return_button = document.getElementById("return");

return_button.addEventListener("click", async () => {
	let token    = localStorage.getItem("token");
	let user_id  = localStorage.getItem("user_id");
	let lobby_id = document.getElementById("lobby_id").innerHTML;

	// Leaving the lobby
	let payload = {
		token   : token,
		user_id : user_id,
		lobby_id: lobby_id
	};
	let response = await server_query("/lobby_leave", "POST", payload);

	if (response.status == response_status.SUCESS) {
		redirect("../html/home.html");
	}
	alert(response.log);
});

/*
 * Clipboard system
 */

const button = document.getElementById("copy_clipboard");

button.addEventListener("click", async () => {
	var copyText = document.getElementById("lobby_id").innerHTML;
	navigator.clipboard.writeText(copyText);
	modal.set_title("Copy to clipboard");
	modal.set_body("Copied " + copyText + " to clipboard");
	modal.show();
});

/*
 * Querying backend to create a lobby.
 */

async function create_lobby(movie_id) {
	let payload = {
		token: localStorage.getItem("token"),
		admin_id: localStorage.getItem("user_id")
	};

	let response = await server_query("/lobby_create", "POST", payload);
	if (response.status == response_status.FAILED) {
		alert(response.log);
		return null;
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
		alert(response.log);
		return null;
	}
	lobby = response.ext[0];
	return lobby;
}


/*
 * Queries the backend to update the host state
 */

async function sync_player(player, lobby_id) {
	let host_state = {
		token    : localStorage.getItem("token"),
		lobby_id : lobby_id,
		host_time: player.currentTime,
		paused   : player.paused,
		playing  : player.playing,
		speed    : player.speed
	};
	let response = await server_query("/lobby_update_host_state", "POST", host_state);
	sync_player(player, lobby_id);
}

window.onload = async () => {
	let id = url_params.get("id");
	let title = url_params.get("title");

	let lobby = await create_lobby(id);
	if (!lobby) {
		//TODO: Show error or something
		alert("Failed to create lobby");

		redirect("../html/home.html");
		return;
	}

	let lobby_id_label = document.getElementById("lobby_id");
	lobby_id_label.innerHTML = lobby.id;

	// Adding the movie link to player
	let source = document.createElement("source");
	source.src = `${server_ip}/get_video?id=${id}`;
	source.type = "video/webm";
	video.appendChild(source);

	// Sending host_state
	const player = new Plyr('#player');
	sync_player(player, lobby.id);
}
