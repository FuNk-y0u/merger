const response_status = {
	SUCESS				: 200,
	FAILED				: 400,
	TOKEN_EXIPRED : 401,
	NO_ADMIN			: 402,
	NOT_FOUND			: 404
};

//const server_ip = "https://merger-dev-pfqf.2.sg-1.fl0.io";
const server_ip = "http://localhost:8080";

const sleep = ms => new Promise(r => setTimeout(r, ms));

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

	return await fetch(server_ip + endpoint, params)
	.then(async (response) => {
		if (response.ok) {
			let result = await response.text();
			let data = JSON.parse(result);
			return data;
		}
		throw new Error(`Failed to fetch at endpoint ${endpoint}`);
	})
	.catch((error) => {
		return {
			log: error,
			status: response_status.FAILED,
			ext: []
		};
	});
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

	let url = `${root_path}/${page_name}/${page_name}.html`;
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

const loose_redirect_parent = async (page_name, params = null) => {
	let root_path = localStorage.getItem("root_path");

	let url = `${root_path}/${page_name}/${page_name}.html`;
	if (params) url += "?" + params;

	parent.window.location.href = url;
}

const redirect_page_parent = async (page_name, params = null) => {
	let res = await auth();
	if (res.status != response_status.SUCESS) {
		alert(res.log);
		return;
	}
	await loose_redirect_parent(page_name, params);
}


function srt_to_vtt(data) {
	// remove dos newlines
	var srt = data.replace(/\r+/g, '');
	// trim white space start and end
	srt = srt.replace(/^\s+|\s+$/g, '');
	// get cues
	var cuelist = srt.split('\n\n');
	var result = "";
	if (cuelist.length > 0) {
		result += "WEBVTT\n\n";
		for (var i = 0; i < cuelist.length; i=i+1) {
			result += convertSrtCue(cuelist[i]);
		}
	}
	return result;
}

function convertSrtCue(caption) {
	// remove all html tags for security reasons
	//srt = srt.replace(/<[a-zA-Z\/][^>]*>/g, '');
	var cue = "";
	var s = caption.split(/\n/);
	// concatenate muilt-line string separated in array into one
	while (s.length > 3) {
		for (var i = 3; i < s.length; i++) {
			s[2] += "\n" + s[i]
		}
		s.splice(3, s.length - 3);
	}
	var line = 0;
	// detect identifier
	if (!s[0].match(/\d+:\d+:\d+/) && s[1].match(/\d+:\d+:\d+/)) {
		cue += s[0].match(/\w+/) + "\n";
		line += 1;
	}
	// get time strings
	if (s[line].match(/\d+:\d+:\d+/)) {
		// convert time string
		var m = s[1].match(/(\d+):(\d+):(\d+)(?:,(\d+))?\s*--?>\s*(\d+):(\d+):(\d+)(?:,(\d+))?/);
		if (m) {
			cue += m[1]+":"+m[2]+":"+m[3]+"."+m[4]+" --> "
						+m[5]+":"+m[6]+":"+m[7]+"."+m[8]+"\n";
			line += 1;
		} else {
			// Unrecognized timestring
			return "";
		}
	} else {
		// file format error or comment lines
		return "";
	}
	// get cue text
	if (s[line]) {
		cue += s[line] + "\n\n";
	}
	return cue;
}

function get_random_int(max) {
	return Math.floor(Math.random() * max);
}

export {
	server_ip,
	sleep,
	server_query,
	response_status,
	auth,
	loose_redirect,
	redirect_page,
	redirect_page_parent,
	srt_to_vtt,
	get_random_int
}
