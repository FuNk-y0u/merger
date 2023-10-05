const response_status = {
	SUCESS        : 200,
	FAILED        : 400,
	TOKEN_EXIPRED : 401,
	NOT_FOUND     : 404
};

const server_ip = "http://127.0.0.1:8000";

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

export { server_ip, server_query, response_status }
