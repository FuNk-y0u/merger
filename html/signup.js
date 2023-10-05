import {
	server_ip,
	server_query,
	response_status
} from "./util.js";
import { Modal } from "./modal.js"

const button = document.getElementById("signup_button");
const modal_root = document.getElementById("modal_root");
const modal = new Modal(modal_root);

button.addEventListener("click", async () => {
	let username = document.getElementById("username").value;
	let email    = document.getElementById("email").value;
	let password = document.getElementById("password").value;
	let con_pass = document.getElementById("con_pass").value;

	// Checking for empty field
	if (!username || !email || !password || !con_pass) {
		modal.set_title("Error!");
		modal.set_body("All input fields must be filled.");
		modal.show();
		return;
	}

	// Checking for confirm password
	if (password != con_pass) {
		modal.set_title("Error!");
		modal.set_body("Password and confirm password didnt match.");
		modal.show();
		return;
	}

	// Server query
	let payload = {
		email: email,
		username: username,
		password: password
	};
	let response = await server_query("/signup", "POST", payload);
	if (response.status == response_status.FAILED) {
		modal.set_title("Signup Error!");
		modal.set_body(response.log);
		modal.show();
		return;
	}

	modal.set_title("Sucess");
	modal.set_body(response.log);
	modal.show();
});
