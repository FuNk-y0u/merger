import { 
    server_ip,
	server_query,
	response_status,
	redirect_page_parent,
	loose_redirect
} from "../../utils.js";

import { Modal } from "../../static/js/modal.js";

const modal = new Modal(
	document.getElementById("modal_root")
);

const join_lobby_button = document.getElementById("join_lobby");
join_lobby_button.addEventListener("click", async () => {
	let lobby_id = document.getElementById("lobby_id").value;
	if (!lobby_id) {
		modal.set_title("Error");
        modal.set_body("Invalid theatre code");
        modal.show();
		return;
	}
    else{
        let params = `id=${lobby_id}&host=0`;
	    redirect_page_parent("theatre", params);
    }
});