import {
	server_ip,
	server_query,
	response_status,
	redirect
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
	let lobby_id = url_params.get("id");

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
 * Queries backend to join the lobby
 */

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

/*
 * Queries backend for host state to syncronize player
 */

async function sync_player(player, lobby_id) {
	let payload = {
		token   : localStorage.getItem("token"),
		lobby_id: lobby_id
	};

	let response = await server_query("/lobby_get_host_state", "POST", payload);
	if (response.status != response_status.SUCESS) {
		alert(response.log);

		// Leaving the lobby
		payload = {
			token   : localStorage.getItem("token"),
			user_id : localStorage.getItem("user_id"),
			lobby_id: lobby_id
		};
		await server_query("/lobby_leave", "POST", payload);

		redirect("../html/home.html");
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

		redirect("../html/home.html");
		return;
	}

	// Adding the movie link to player
	//let source = document.createElement("source");
	//source.src = `${server_ip}/get_video?id=${lobby.movie_id}`;
	//source.type = "video/webm";
	//video.appendChild(source);

	let res = await server_query("/get_video", "POST", { video_id: lobby.movie_id});
	if (res.status != response_status.SUCESS) {
		alert(res.log);
		redirect("../html/home.html");
		return;
	}
	let url = res.ext[0]

	const video = document.getElementById("player");
	const player = new Plyr('#player', {
		listeners: {
			seek: function (e) {
				e.preventDefault()
				return false
			}
		}
	});

	let source = await extract_m3u8_pl(url);

	if (!Hls.isSupported()) {
		video.src = source;
	} else {
		const hls = new Hls();
		hls.loadSource(source);
		hls.attachMedia(video);
		window.hls = hls;
	}
	window.player = player;

	sync_player(player, lobby.id);
}
