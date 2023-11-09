import {
	server_ip,
	server_query,
	response_status,
	redirect_page,
	sleep,
	get_random_int
} from "./../../utils/utils.js";
import { Modal } from "./../../utils/modal.js"

import {
	join_lobby,
	create_lobby
} from "./lobby_api.js"
import { Player } from "./player.js"

const colors = ["#0d6efd", "#ff4f4f", "#5cb038"]
const modal = new Modal(
	document.getElementById("modal_root")
);

/*
 * Extracts parameters from url
 */

const get_url_params = () => {
	const url_params = new URLSearchParams(window.location.search);
	return {
		id: url_params.get("id"),
		host: parseInt(url_params.get("host"))
	};
}


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
		redirect_page("home");
		return;
	}
	alert(response.log);
});


/*
 * Clipboard system
 */

const button = document.getElementById("copy_clipboard");
button.addEventListener("click", async () => {
	let copy_text = document.getElementById("lobby_id").innerHTML;
	navigator.clipboard.writeText(copy_text);
	modal.set_title("Copy to clipboard");
	modal.set_body("Copied " + copy_text+ " to clipboard");
	modal.show();
});


/*
 * Lobby system
 */

const handle_lobby = async (params) => {
	const lobby_id_card  = document.getElementById("lobby_id_card");

	let lobby, log;
	if (params.host) {
		[lobby, log] = await create_lobby(params.id);
		lobby_id_card.style.visibility = "visible";
	} else {
		[lobby, log] = await join_lobby(params.id);
		lobby_id_card.style.visibility = "hidden";
	}

	if (!lobby) {
		alert(log);
		return null;
	}

	const lobby_id_label = document.getElementById("lobby_id");
	lobby_id_label.innerHTML = lobby.id;

	return lobby;
}


/*
 * Video system
 */

const get_video = async (video_id) => {
	let res = await server_query("/get_video", "POST", { video_id: video_id });
	if (res.status != response_status.SUCESS) {
		alert(res.log);
		return null;
	}
	return res.ext[0];
}

const update_watch_list = async (id) => {
	let payload = {
		token: localStorage.getItem("token"),
		lobby_id: id
	}

	let res = await server_query("/lobby_get_members", "POST", payload);
	
	if (res.status != response_status.SUCESS)
	{
		alert(res.log);
		redirect_page("home");
		return;
	}

	let members = res.ext;
	console.log(members);
	const watch_list_table = document.getElementById("watch_list");
	watch_list_table.innerHTML = "";
	members.forEach(element => {

		watch_list_table.innerHTML += `
			<tr>
				<td> <i class="fa-solid fa-user" style="color: ${colors[get_random_int(3)]};"></i> </td>
				<td> ${element} </td>
			</tr>
		`
	});
	sleep(3000);
	update_watch_list(id);
}

const render_lobby = async () => {
	let params = get_url_params();

	let lobby = await handle_lobby(params);
	
	if (!lobby) {
		redirect_page("home");
		return;
	}

	update_watch_list(lobby.id);

	// Getting video from backend
	let video = await get_video(lobby.movie_id);
	let url = video.url;
	let subtitle = video.subtitle;

	if (!url) {
		redirect_page("home");
		return;
	}

	let player = new Player("player", params.host, url, subtitle, () => {
		document.getElementById("media_loading").style.display = 'none';
		document.getElementById("frame").style.display = 'flex';
	});

	player.init(() => {
		player.sync(lobby.id);
	});
}

window.onload = render_lobby();
