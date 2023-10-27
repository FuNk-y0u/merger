import { decrypt } from "./decoder.js"

const server_url = "https://www.filemoon.sx"

const get_html = async (url) => {
	return await fetch(url, { method: "GET" })
	.then(async (response) => {
		if (response.ok) {
			let html = await response.text();
			return html;
		}
	})
	.catch((error) => {
		console.log(error);
	});
}

const json_to_xform = (json) => {
	let values = [];
	Object.keys(json).forEach(key => {
		values.push(`${key}=${json[key]}`);
	});
	return values.join("&");
}

const str_to_json = (str) => {
	let json = {};

	str
		.replace(/["']/g, "")
		.slice(1, -1)
		.split(",")
		.forEach(entry => {
			let [key, value] = entry.split(":");
			json[key] = value;
		});

	return json;
}

const get_script_from_html = (html) => {
	let parser = new DOMParser();
	let doc = parser.parseFromString(html, "text/html");
	let script = doc.querySelectorAll('[data-cfasync="false"]')[0];
	return script.innerHTML;
}

const get_post_data_from_jquery = (jquery) => {
	jquery = jquery.replaceAll(";", ";\n");
	let lines = jquery.split("\n");

	for (let i in lines) {
		let line = lines[i];
		if (line.includes("var postData")) {
			let json_value = line.split("=")[1].replace(";", "");
			let post_data = str_to_json(json_value);
			return post_data;
		}
	}
}

const get_file_info = async (post_data) => {
	let payload = json_to_xform(post_data);
	let params = {
		method: "POST",
		headers: {
			"Accept": "*/*",
			"Content-Type": "application/x-www-form-urlencoded",
			"Content-Length": payload.length,
			"Connection": "keep-alive",
			"Host": "www.filemoon.sx"
		},
		body: payload
	};

	return await fetch(server_url + "/dl", params)
	.then(async (response) => {
		if (response.ok) {
			let json = await response.json();
			return json[0];
		}
	})
	.catch((error) => {
		console.log(error);
	});
}

const get_pl_url = (file_info) => {
	let chars = {
		'0': '5',
		'1': '6',
		'2': '7',
		'5': '0',
		'6': '1',
		'7': '2'
	};

	let seed = file_info.seed.replace(/[012567]/g, m => chars[m]);
	let url = decrypt(file_info.file, seed);
	url = url.replace(/[012567]/g, m => chars[m]);
	return url;
}

const extract_m3u8_pl = async (url) => {
	let html = await get_html(url);
	let script = get_script_from_html(html);
	let jquery = eval(script.replace("eval", ""));
	let post_data = get_post_data_from_jquery(jquery);
	let file_info = await get_file_info(post_data);
	url = get_pl_url(file_info);
	return url;
}

export {
	extract_m3u8_pl
};
