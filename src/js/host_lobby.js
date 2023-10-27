import {
	server_ip,
	server_query,
	response_status,
	redirect,
} from "./util.js";
import { Modal } from "./modal.js"
import { extract_m3u8_pl } from "./extractor.js"

const url_params = new URLSearchParams(window.location.search);

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
		return;
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
const create_lobby = async (movie_id) => {
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

const sync_player = async (player, lobby_id) => {
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

	let res = await server_query("/get_video", "POST", { video_id: id });
	if (res.status != response_status.SUCESS) {
		alert(res.log);
		redirect("../html/home.html");
		return;
	}
	let url = res.ext[0]

	const video = document.getElementById("player");
	const player = new Plyr('#player');

	let source = await extract_m3u8_pl(url);
	console.log(source);

	if (!Hls.isSupported()) {
		video.src = source;
	} else {
		const hls = new Hls();
		hls.loadSource(source);
		hls.attachMedia(video);
		window.hls = hls;
	}
	window.player = player;

	// Sending host_state
	sync_player(player, lobby.id);
}
