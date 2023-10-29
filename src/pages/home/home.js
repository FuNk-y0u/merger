import {
	server_ip,
	server_query,
	response_status,
	redirect_page
} from "./../../utils/utils.js";
import { Modal } from "./../../utils/modal.js"

const modal = new Modal(
	document.getElementById("modal_root")
);


/*
 * Joining lobby system
 */

const join_lobby_button = document.getElementById("join_lobby");
join_lobby_button.addEventListener("click", () => {
	let lobby_id = document.getElementById("lobby_id").value;
	if (!lobby_id) {
		modal.set_title("Error");
		modal.set_body("Lobby id cannot be empty.");
		modal.show();
		return;
	}

	let params = `id=${lobby_id}&host=0`;
	redirect_page("lobby", params);
});


/*
 * Coming soon page redirection
 */

const coming_soon_redirect = document.getElementById("coming_soon_redirect");
coming_soon_redirect.addEventListener("click", () => {
	redirect_page("coming_soon");
});


/*
 * Video card system
 */

const add_event_listener = (element, videos) => {
	element.addEventListener("click", () => {
		let id = element.id;
		let title = videos[id].title;
		let params = `id=${id}&host=1`;
		redirect_page("lobby", params);
	});
}

const create_video_card = (video_id, video) => {
	const video_card = document.createElement("div");
	video_card.setAttribute("id", video_id);
	video_card.setAttribute("class", "show")

	const thumbnail = document.createElement("img");
	thumbnail.setAttribute("class", "thumbnail");
	thumbnail.src = video.poster_url;

	const title = document.createElement("p");
	title.setAttribute("class","title");
	title.innerHTML = video.title;

	video_card.appendChild(thumbnail);
	video_card.appendChild(title);
	return video_card;
}

const render_video_cards = async () => {
	const movie_grid = document.getElementById("movie_grid");
	movie_grid.innerHTML = "";

	let response = await server_query("/get_video_list?uploaded=True", "GET", {});
	if (response.status != response_status.SUCESS) {
		modal.set_title("Error");
		modal.set_body(response.log);
		modal.show();
		return;
	}

	let videos = response.ext[0]
	for (let video_id in videos) {
		const video_card = create_video_card(video_id, videos[video_id]);
		movie_grid.appendChild(video_card);

		add_event_listener(video_card, videos);
	}
}

window.onload = render_video_cards;
