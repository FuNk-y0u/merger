import { Modal } from "../../static/js/modal.js";

import {
	server_ip,
	server_query,
	response_status,
	redirect_page,
	sleep,
	get_random_int
} from "../../utils.js";

import {
	join_lobby,
	create_lobby
} from "./lobby_api.js";

import { Player } from "./player.js"

let update=true;

const modal = new Modal(
	document.getElementById("modal_root")
);

// * Copy to clipboard system
let copy_button = document.querySelector("#copy_button");
copy_button.addEventListener("click", () => {
	let copy_text = document.getElementById("lobby_code_text").innerHTML;
	navigator.clipboard.writeText(copy_text);
	modal.set_title("Copy to clipboard");
	modal.set_body("Copied " + copy_text+ " to clipboard");
	modal.show();
});

// * Movie metada section
const setup_movie_metadata = async (video_id) => {
	let response = await server_query("/get_video_metadata", "POST", {video_id});
	if(response.status == response_status.SUCESS){
		let video = response.ext[0];
		document.getElementById("movie_title").innerHTML = video.title;
    	document.getElementById("movie_image").src = video.poster_url;
    	document.getElementById("movie_description").innerHTML = video.description;
	}
}


// * Lobby Section
const handle_lobby = async (params) => {
	const lobby_id_card  = document.getElementById("lobby_code");

	let lobby, log;
	if (params.host) {
		[lobby, log] = await create_lobby(params.id);
		lobby_id_card.style.visibility = "visible";
	} else {
		[lobby, log] = await join_lobby(params.id);
		lobby_id_card.style.visibility = "hidden";
	}

	if (!lobby) {
		modal.set_title("Error");
        modal.set_body(log);
        modal.show();
		return null;
	}

	const lobby_id_label = document.getElementById("lobby_code_text");
	lobby_id_label.innerHTML = lobby.id;

	return lobby;
}

const leave_lobby = async () => {
	let token    = localStorage.getItem("token");
	let user_id  = localStorage.getItem("user_id");
	let lobby_id = document.getElementById("lobby_code_text").innerHTML;
    console.log(lobby_id);

	// Leaving the lobby
	let payload = {
		token   : token,
		user_id : user_id,
		lobby_id: lobby_id
	};
	let response = await server_query("/lobby_leave", "POST", payload);

	if (response.status == response_status.SUCESS) {
		redirect_page("index");
		return;
	}
	modal.set_title("Error");
    modal.set_body(response.log);
    modal.show();
}

const update_lobby = async (player, lobby_id) => {
	while (update) {
		let res = await update_watch_list(lobby_id);
		if (res.status != response_status.SUCESS) {
			modal.set_title("Error");
            modal.set_body(res.log);
            modal.show();
			return;
		}

		res = await player.sync(lobby_id);
		if (res.status != response_status.SUCESS) {
			modal.set_title("Error");
            modal.set_body(res.log);
            modal.show();
			return;
		}
	}
}


// * Leave lobby section
const return_button = document.getElementById("leave_lobby");

return_button.addEventListener("click", async () => {
	update = false;
});


// * Watch list section
const update_watch_list = async (id) => {
	let payload = {
		token: localStorage.getItem("token"),
		lobby_id: id
	}

	let res = await server_query("/lobby_get_members", "POST", payload);
	if (res.status == response_status.SUCESS) {
		const watch_list_table = document.getElementById("viewers");
		watch_list_table.innerHTML = "";

		let members = res.ext;
		members.forEach(element => {
			watch_list_table.innerHTML += `
                <div class="viewer">
                    <i class="fa-solid fa-user"></i> <div id="viewer_username">${element}</div>
                </div>
			`
		});
	}
	return res;
}

// * URL Section
const get_url_params = () => {
    const url_params = new URLSearchParams(window.location.search);
    
    return {
        id: url_params.get("id"),
        host: parseInt(url_params.get("host"))
    }
}

// * Video section
const get_video = async (video_id) => {
	setup_movie_metadata(video_id);
	let res_metadata = await server_query("/get_video_metadata", "POST", { video_id: video_id });
	let res = await server_query("/get_video", "POST", { video_id: video_id });
	if (res.status != response_status.SUCESS) {
		console.log(res.log);
		return null;
	}
	return res.ext[0];
}


// * Render section
const render_lobby = async () => {
	let params = get_url_params();

	let lobby = await handle_lobby(params);
	
	if (!lobby) {
		redirect_page("index");
		return;
	}

	// Getting video from backend
	let video = await get_video(lobby.movie_id);
	let url = video.url;
	let subtitle = video.subtitle;

	if (!url) {
		redirect_page("index");
		return;
	}

	let player = new Player("player", params.host, url, subtitle, () => {
		document.getElementById("load_indicator").style.display = 'none';
		document.getElementById("video_frame").style.display = 'block';
	});

	await player.init();
	await update_lobby(player, lobby.id);
	await leave_lobby();
}

window.onload = () =>{
    render_lobby();
}