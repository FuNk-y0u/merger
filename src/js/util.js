const response_status = {
	SUCESS        : 200,
	FAILED        : 400,
	TOKEN_EXIPRED : 401,
	NO_ADMIN      : 402,
	NOT_FOUND     : 404
};

const server_ip = "https://merger-dev-mngs.2.sg-1.fl0.io";
//const server_ip = "http://localhost:8080";

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

const redirect = async (path) => {
	let res = await auth();
	if (res.status != response_status.SUCESS) {
		// TODO: Show some error
		alert("Failed to authenticate");
		return;
	}

	window.location.href = path;
}

export {
	server_ip,
	server_query,
	response_status,
	auth,
	redirect
}
