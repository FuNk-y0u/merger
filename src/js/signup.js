import {
	server_ip,
	server_query,
	response_status,
	redirect
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

	// Loging in
	response = await server_query("/login", "POST", payload);
	if (response.status == response_status.FAILED) {
		modal.set_title("Login Error!");
		modal.set_body(response.log);
		modal.show();
		return;
	}

	// Saving the token
	let token = response.ext[0].token;
	localStorage.setItem("token", token);

	// Redirect
	redirect("../html/loading.html");
});
