import { Modal } from "../../static/js/modal.js";

const modal = new Modal(
	document.getElementById("modal_root")
);

const movie_selector_modal = new bootstrap.Modal(
	document.getElementById("movie_selection_modal")
);

import {
	server_ip,
	server_query,
	response_status,
	redirect_page,
	sleep,
	get_random_int,
    redirect_page_parent
} from "../../utils.js";


const per_page = 10;
let total_page_cnt = 0;
let page_no = 1;

const get_total_page_cnt = async () => {
	let payload = {
		uploaded: true,
		per_page: per_page
	};
	let response = await server_query("/get_total_page_cnt", "POST", payload);
	return response.ext[0];
}


let paginate_left = document.querySelector("#pagination_left");
let paginate_right = document.querySelector("#pagination_right");
let page_no_div = document.querySelector("#pagination_data");

paginate_left.addEventListener("click", () => {
    if(page_no > 1){
        page_no -= 1;
        page_no_div.innerHTML = page_no;
        render_video_cards();
    }
})

paginate_right.addEventListener("click", () => {
    if(page_no < total_page_cnt){
        page_no += 1;
        page_no_div.innerHTML = page_no;
        render_video_cards();
    }
})

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

let add_button = document.querySelector("#add_movie_button");
let search_bar = document.querySelector(".search_bar");

search_bar.addEventListener("keypress", (e) => {
	if (e.key == "Enter") {
		e.preventDefault();
		add_button.click();
	}
})

add_button.addEventListener('click', async() => {
    const movie_selector_body = document.getElementById("movie_selector_body");
	movie_selector_body.innerHTML = ""
    let movie_name = search_bar.value;
    if (!movie_name) {
		modal.set_title("Error");
		modal.set_body("Movie name cannot be empty.");
		modal.show();
		return;
	}

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
    document.getElementById("loading_animation").style.display = 'none';

    let movies = response.ext[0];
    console.log(movies)
    for (let movie_id in movies) {
		const video_card = create_video_card(movie_id, movies[movie_id]);
		movie_selector_body.appendChild(video_card);

		add_event_listener(video_card, movies);
	}
})

const create_video_card = (video_id, video) => {
    const video_card = document.createElement("div");
    video_card.setAttribute("class", "show");
    video_card.setAttribute("id", video_id);

    let show_div_xml = `
    <div class="non_eager_div">
        <!-- Movie Image -->
        <img src="${video.poster_url}" loading="lazy" id="movie_image">
        <!-- Movie Title -->
        <div id="movie_title">${video.title}</div>
    </div>
    `

    video_card.innerHTML = show_div_xml;
    return video_card;

}


/*
 * Queries the backend for comming soon movies and displays them in grid.
 */

const render_video_cards = async () => {
	const movie_grid = document.getElementById("movie_grid");

	let params = {
		uploaded: false,
		page_no : page_no,
		per_page: per_page
	};

	let response = await server_query("/get_video_list", "POST", params);
	if (response.status == response_status.FAILED) {
		modal.set_title("Error");
		modal.set_body(response.log);
		modal.show();
		return;
	}

    movie_grid.innerHTML = "";
	let videos = response.ext[0]
	for (let video_id in videos) {
		const video_card = create_video_card(video_id, videos[video_id]);
		movie_grid.appendChild(video_card);
	}
}

window.onload = async () => {
	total_page_cnt = await get_total_page_cnt();
	render_video_cards();
}
