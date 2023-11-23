import {
	server_ip,
	server_query,
	response_status,
	redirect_page,
	loose_redirect
} from "../../utils.js"

let accountName = document.querySelector("#account_name");
let accountId = document.querySelector("#account_id");
let accountEmail = document.querySelector("#account_email");
let logoutButton = document.querySelector("#logout_button")
window.onload = () => {
    accountName.innerHTML = localStorage.getItem("username");
    accountId.innerHTML = localStorage.getItem("user_id");
    accountEmail.innerHTML = localStorage.getItem("email");
}

logoutButton.addEventListener('click', () => {
    localStorage.removeItem("token");
	localStorage.removeItem("email");
	localStorage.removeItem("user_id");
	localStorage.removeItem("username");
	parent.window.location.href = "../login/login.html";
})