import { 
		server_ip,
	server_query,
	response_status,
	redirect_page_parent,
	loose_redirect
} from "../../utils.js";

let movie_grid = document.getElementById("movie_grid");

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
		render_show_cards();
	}
})

paginate_right.addEventListener("click", () => {
	console.log(total_page_cnt);
	if(page_no < total_page_cnt){
		page_no += 1;
		page_no_div.innerHTML = page_no;
		render_show_cards();
	}
})

const create_show_card = (show_id, show) => {
	let show_div_xml = `
		<!-- Non Hovered Movie-->
		<div class="non_eager_div">
			<!--	Movie Image -->
			<img src="${show.poster_url}" loading="lazy" id="movie_image">
			<!--	Movie Title -->
			<div id="movie_title">${show.title}</div>
		</div>

		<!--	Hovered Movie With Discription -->
		<div class="eager_div">
			<table>
				<tr>
					<div class="eager_items">
						<!--	Movie Image -->
						<td><img src="${show.poster_url}" loading="lazy" id="movie_image"></td>
						<!-- Movie Title -->
						<td>
							<h1 id="movie_title">${show.title}</h1>
							<!-- Movie Description -->
							<p class="description" id="movie_description">
							${show.description}
							</p>
						</td>
					</div>
				</tr>
			</table>	 
		</div>
	`;
	const show_card = document.createElement("div");
	show_card.setAttribute("id", show_id);
	show_card.setAttribute("class", "show");
	show_card.setAttribute("onmouseenter","on_hover(this.id);");
	show_card.setAttribute("onmouseleave","on_leave(this.id);");

	show_card.innerHTML = show_div_xml;
	return show_card;
}
const add_event_listener = (element, shows) => {
	element.addEventListener("click", () => {
		let id = element.id;
		let title = shows[id].title;
		let poster_url = shows[id].poster_url;
		let description = shows[id].description;
		let params = `id=${id}&host=1&title=${title}&poster_url=${poster_url}&description=${description}`;
		redirect_page_parent("theatre", params);
	});
}

const render_show_cards = async () => {
	let params= {
		uploaded: true,
		page_no : page_no,
		per_page: per_page
	};

	let response = await server_query("/get_video_list", "POST", params);
	if(response.status != response_status.SUCESS){
		console.log(response.log);
		return;
	}

	let shows = response.ext[0];
	movie_grid.innerHTML = "";
	for(let show_id in shows){
		const show_card = create_show_card(show_id, shows[show_id]);
		movie_grid.appendChild( show_card);
		add_event_listener(show_card, shows);
	}
}


const search_button = document.getElementsByClassName("search_button")[0]
const search_bar = document.getElementsByClassName("search_bar")[0]

search_bar.addEventListener("keypress", (e) => {
	if (e.key == "Enter") {
		e.preventDefault();
		search_button.click();
	}
})

search_button.addEventListener("click", async () => {
	let payload = {
		title: search_bar.value
	};

	let response = await server_query("/search_video", "POST", payload);
	if (response.status != response_status.SUCESS) {
		movie_grid.innerHTML = "";
		document
			.getElementById("error_msg")
			.innerHTML = response.log;
		return;
	}

	let shows = response.ext[0];
	movie_grid.innerHTML = "";
	for(let show_id in shows){
		const show_card = create_show_card(show_id, shows[show_id]);
		movie_grid.appendChild( show_card);
		add_event_listener(show_card, shows);
	}
})


window.onload = async () => {
	total_page_cnt = await get_total_page_cnt();
	render_show_cards();
}
