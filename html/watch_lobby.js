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

async function join_lobby(lobby_id) {
	let payload = {
		token   : localStorage.getItem("token"),
		lobby_id: lobby_id,
		user_id : localStorage.getItem("user_id")
	};

	let response = await server_query("/lobby_join", "POST", payload);
	if (response.status == response_status.FAILED) {
		alert(response.log);
		return null;
	}

	let lobby = response.ext[0];
	return lobby;
}

async function sync_player(player, lobby_id) {
	let payload = {
		token   : localStorage.getItem("token"),
		lobby_id: lobby_id
	};

	let response = await server_query("/lobby_get_host_state", "POST", payload);
	if (response.status != response_status.SUCESS) {
		modal.set_title("Server error");
		modal.set_body(response.log);
		modal.show();
		return;
	}

	let host_state = response.ext[0];

	if ((host_state.host_time - player.currentTime) > 1 || (host_state.host_time - player.currentTime) < -1) {
		player.currentTime = host_state.host_time;
	}
	if (host_state.paused) {
		player.pause();
	}
	if (host_state.playing) {
		player.play();
	}
	player.speed = host_state.speed;

	sync_player(player, lobby_id);
}

window.onload = async () => {
	let lobby_id = url_params.get("id");
	let lobby = await join_lobby(lobby_id);
	if (!lobby) {
		//TODO: Show error or something
		alert("Failed to join lobby.");

		redirect("home.html");
		return;
	}

	// Adding the movie link to player
	let source = document.createElement("source");
	source.src = `${server_ip}/get_video?id=${lobby.movie_id}`;
	source.type = "video/webm";
	video.appendChild(source);

	// Syncronizing player
	const player = new Plyr('#player', {
		listeners: {
			seek: function (e) {
				e.preventDefault()
				return false
			}
		}
	});

	sync_player(player, lobby.id);
}
