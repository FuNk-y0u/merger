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
const movie_selector_modal = new bootstrap.Modal(
	document.getElementById("movie_selection_modal")
);


/*
 * Return button
 */

const return_button = document.getElementById("return");
return_button.addEventListener("click", () => {
	redirect_page("home");
});


/*
 * Queries the backend to save the selected movie to the comming soon page.
 */

const add_event_listener = (element, movies) => {
	element.addEventListener("click", async () => {
		let id = element.id;
		let payload = movies[element.id];
		payload.token =  localStorage.getItem("token")

		// Quering the backend to save the new movie
		let response = await server_query("/add_new_movie", "POST", payload);

		movie_selector_modal.hide();

		modal.set_title("Sucess");
		if (response.status != response_status.SUCESS) {
			modal.set_title("Error");
		}
		modal.set_body(response.log);
		modal.show();

		await render_video_cards();
	});
}


/*
 * Generates video card ui
 */

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


/*
 * Queries backend with movie name and displays the closest results
 */

const add_movie_button = document.getElementById("add_movie");
add_movie.addEventListener("click", async () => {
	const movie_selector_body = document.getElementById("movie_selector_body");
	movie_selector_body.innerHTML = ""

	let movie_name = document.getElementById("movie_name").value;
	if (!movie_name) {
		modal.set_title("Error");
		modal.set_body("Movie name cannot be empty.");
		modal.show();
		return;
	}

	// Quering the backend for the result
	let payload = {
		token: localStorage.getItem("token"),
		movie_name: movie_name
	};
	let response = await server_query("/search_new_movie", "POST", payload);

	if (response.status != response_status.SUCESS) {
		modal.set_title("Error");
		modal.set_body(response.log);
		modal.show();
		return;
	}

	// Creating thumbnails for movie selector pannel
	let movies = response.ext[0];
	for (let movie_id in movies) {
		const video_card = create_video_card(movie_id, movies[movie_id]);
		movie_selector_body.appendChild(video_card);

		add_event_listener(video_card, movies);
	}
});


/*
 * Queries the backend for comming soon movies and displays them in grid.
 */

const render_video_cards = async () => {
	const movie_grid = document.getElementById("movie_grid");
	movie_grid.innerHTML = "";

	let params = {
		uploaded: false,
		page_no: 1,
		per_page: 10
	};

	let response = await server_query("/get_video_list", "POST", params);
	if (response.status == response_status.FAILED) {
		modal.set_title("Error");
		modal.set_body(response.log);
		modal.show();
		return;
	}

	let videos = response.ext[0]
	for (let video_id in videos) {
		let video = videos[video_id];
		const video_card = create_video_card(video_id, videos[video_id]);
		movie_grid.appendChild(video_card);
	}
}

window.onload = render_video_cards;
