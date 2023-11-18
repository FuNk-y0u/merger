import { Modal } from "../../static/js/modal.js";
const modal = new Modal(
	document.getElementById("modal_root")
);

let add_button = document.querySelector("#add_movie_button");
add_button.addEventListener('click', () => {
    modal.set_title(`Search results for "${document.querySelector(".search_bar").value}"`);
    modal.set_body(`
        <!-- movies section -->
        <div class="movie_grid_modal">

            <!-- MOVIE DISPLAY TEMPLATE -->
            <div class="show_modal" id="[movie_id_here]">
                <!-- Non Hovered Movie-->
                <div class="non_eager_div">
                    <img src="../../static/images/template_movie.jpg" loading="lazy" id="movie_image">
                    <div id="movie_title">Spiderman: No way home</div>
                </div>
            </div>
            <!-- MOVIE DISPLAY TEMPLATE -->
            <div class="show_modal" id="[movie_id_here]">
                <!-- Non Hovered Movie-->
                <div class="non_eager_div">
                    <img src="../../static/images/template_movie.jpg" loading="lazy" id="movie_image">
                    <div id="movie_title">Spiderman: No way home</div>
                </div>
            </div>

        </div>
    `);
    modal.show();
})