const response_status = {
	SUCESS        : 200,
	FAILED        : 400,
	TOKEN_EXIPRED : 401,
	NO_ADMIN      : 402,
	NOT_FOUND     : 404
};

//const server_ip = "https://merger-dev-mngs.2.sg-1.fl0.io";
const server_ip = "https://merger-dev-pfqf.2.sg-1.fl0.io";

const sleep = ms => new Promise(r => setTimeout(r, ms));

//TODO: Rewrite server query
const server_query = async (endpoint, method, payload) => {
	let params = {
		method: method,
		headers: {
			"Content-Type": "application/json",
			"Accept": "application/json"
		},
	};

	if (method != "GET") {
		params.body = JSON.stringify(payload);
	}

	const request = await fetch(server_ip + endpoint, params);
	let result = await request.text();
	let data = JSON.parse(result);
	return data;
}

const auth = async () => {
	let payload = {
		token: localStorage.getItem("token")
	};
	let response = await server_query("/auth", "POST", payload);

	if (response.status == response_status.SUCESS) {
		let user = response.ext[0];
		localStorage.setItem("user_id", user.id);
		localStorage.setItem("email", user.email);
		localStorage.setItem("username", user.username);
		return response;
	}
	return response;
}

const loose_redirect = async (page_name, params = null) => {
	let root_path = localStorage.getItem("root_path");

	let url = `${root_path}/pages/${page_name}/${page_name}.html`;
	if (params) url += "?" + params;

	window.location.href = url;
}

const redirect_page = async (page_name, params = null) => {
	let res = await auth();
	if (res.status != response_status.SUCESS) {
		alert(res.log);
		return;
	}
	await loose_redirect(page_name, params);
}

export {
	server_ip,
	sleep,
	server_query,
	response_status,
	auth,
	loose_redirect,
	redirect_page
}
