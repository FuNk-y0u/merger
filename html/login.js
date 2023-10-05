import {
	server_ip,
	server_query,
	response_status
} from "./util.js";
import { Modal } from "./modal.js"

const button = document.getElementById("login_button");
const modal_root = document.getElementById("modal_root");
const modal = new Modal(modal_root);

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
	if (response.status == response_status.FAILED) {
		modal.set_title("Login Error!");
		modal.set_body(response.log);
		modal.show();
		return;
	}

	// Saving the token
	let token = response.ext[0].token;
	console.log(token);
	localStorage.setItem("token", token);

	// Redirect
	window.location.href="loading.html"
});
