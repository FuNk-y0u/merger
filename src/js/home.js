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
	movie_grid.innerHTML = "";

	let response = await server_query("/get_video_list?uploaded=True", "GET", {});
	if (response.status == response_status.FAILED) {
		modal.set_title("Error");
		modal.set_body(response.log);
		modal.show();
		return;
	}

	let videos = response.ext[0]
	for (let video_id in videos) {
		let video = videos[video_id];

		let pannel = document.createElement("div");
		pannel.setAttribute("id", video_id);
		pannel.setAttribute("class","show")

		let thumbnail = document.createElement("img");
		thumbnail.setAttribute("class", "thumbnail");
		thumbnail.src = video.poster_url;

		let title = document.createElement("p");
		title.setAttribute("class","title");
		title.innerHTML = video.title;

		pannel.appendChild(thumbnail);
		pannel.appendChild(title);
		movie_grid.appendChild(pannel);

		add_event_listener(pannel, videos);
	}
}
