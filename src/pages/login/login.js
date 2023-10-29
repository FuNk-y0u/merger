import {
	server_ip,
	server_query,
	response_status,
	redirect_page,
	loose_redirect
} from "./../../utils/utils.js"
import { Modal } from "./../../utils/modal.js"

const modal = new Modal(
	document.getElementById("modal_root")
);


/*
 * Signup page redirection
 */

const anchor = document.getElementById("signup");
anchor.addEventListener("click", async () => {
	loose_redirect("signup");
});


/*
 * Login system
 */

const button = document.getElementById("login_button");
button.addEventListener("click", async () => {
	let email    = document.getElementById("email").value;
	let password = document.getElementById("password").value;

	// Checking for empty field
	if (!email || !password) {
		modal.set_title("Error!");
		modal.set_body("All input fields must be filled.");
		modal.show();
		return;
	}

	// Server query
	let payload = {
		email: email,
		password: password
	};
	let response = await server_query("/login", "POST", payload);
	if (response.status != response_status.SUCESS) {
		modal.set_title("Login Error!");
		modal.set_body(response.log);
		modal.show();
		return;
	}

	// Saving the token
	let token = response.ext[0].token;
	localStorage.setItem("token", token);

	// Redirect
	redirect_page("loading");
});
