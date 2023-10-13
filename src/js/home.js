import {
	server_ip,
	server_query,
	response_status,
	redirect
} from "./util.js";
import { Modal } from "./modal.js"

const movie_grid = document.getElementById("movie_grid");
const modal_root = document.getElementById("modal_root");
const modal = new Modal(modal_root);

// Join lobby
const join_lobby_button = document.getElementById("join_lobby");

join_lobby_button.addEventListener("click", () => {
	let lobby_id = document.getElementById("lobby_id").value;
	if (!lobby_id) {
		modal.set_title("Error");
		modal.set_body("Lobby id cannot be empty.");
		modal.show();
		return;
	}

	redirect(`../html/watch_lobby.html?id=${lobby_id}`);
});

// Video card
function add_event_listener(element, movies) {
	element.addEventListener("click", () => {
		let id = element.id;
		let title = movies[element.id];
		redirect(`../html/host_lobby.html?id=${id}&title=${title}`);
	});
}

window.onload = async () => {
	let response = await server_query("/get_video_list", "GET", {});
	if (response.status == response_status.FAILED) {
		modal.set_title("Error");
		modal.set_body(response.log);
		modal.show();
		return;
	}

	let videos = response.ext[0]
	for (let video in videos) {

		// *! Remove some unnecessary codes - Rob

		let pannel = document.createElement("div");
		pannel.setAttribute("id", video);

		let thumbnail = document.createElement("div");
		thumbnail.setAttribute("id", "show");

		let title = document.createElement("p");
		title.innerHTML = videos[video];

		pannel.appendChild(thumbnail);
		pannel.appendChild(title);
		movie_grid.appendChild(pannel);

		add_event_listener(pannel, videos);
	}
}
