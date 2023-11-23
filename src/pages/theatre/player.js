import {
	server_ip,
	server_query,
	response_status,
	redirect_page,
	srt_to_vtt,
	sleep
} from "../../utils.js";
import { extract_m3u8_pl } from "../../utils/extractor.js";
import { Modal } from "../../static/js/modal.js";
const modal = new Modal(
	document.getElementById("modal_root")
);

class Player {
	constructor(player_id, host, url, subtitle, callback) {
		this.host = host;
		this.url = url;
		this.subtitle = subtitle;

		this.video = document.getElementById(player_id);
		this.player = this.create_plyr_player(player_id, host);
		this.player.on("canplay", () => {
			callback();
		})
	}

	async init() {
		const source = await extract_m3u8_pl(this.url);
		this.attach_hls(source);
		await this.add_subtitle();
	}

	async add_subtitle() {
		if (!this.subtitle) {
			console.log("no subtitles found");
			return;
		}

		let srt_file = await fetch(this.subtitle, { method: "GET" })
			.then(async (response) => {
				if (response.ok) {
					let zip = await response.blob();
					return JSZip.loadAsync(zip).then((content) => {
						return Object.values(content.files)[0].async("text");
					});
				}
				return null;
			})

		if (!srt_file) return;

		let vtt_file = srt_to_vtt(srt_file);

		let track = document.getElementById("track").track;
		track.mode = "showing";

		const parser = new WebVTTParser();
		const tree = parser.parse(vtt_file, "metadata");
		const cues = tree.cues;
		cues.forEach((cue) => {
			track.addCue(new VTTCue(cue.startTime, cue.endTime, cue.text));
		});
	}

	async sync(lobby_id) {
		if (this.host) {
			let res = await this.sync_host_player(lobby_id);
			return res;
		} else {
			let res = await this.sync_watcher_player(lobby_id);
			return res;
		}
	}

	create_plyr_player(player_id, host) {
		let params = {
			controls: ['play-large', 'play', 'progress', 'current-time', 'captions', 'volume', 'fullscreen', 'settings']
		};
		if (!host) {
			params.listeners =  {
				seek: function (e) {
					e.preventDefault();
					return false;
				}
			}
		}
		console.log(player_id);
		const player = new Plyr(`#${player_id}`, params);
		return player;
	}

	attach_hls(source) {
		if (!Hls.isSupported()) {
			this.video.src = source;
		} else {
			const hls = new Hls();
			hls.loadSource(source);
			hls.attachMedia(this.video);
			window.hls = hls;
		}
		window.player = player;
	}

	async sync_host_player(lobby_id) {
		let host_state = {
			token    : localStorage.getItem("token"),
			lobby_id : lobby_id,
			host_time: this.player.currentTime,
			paused   : this.player.paused,
			playing  : this.player.playing,
			speed    : this.player.speed
		};
		let response = await server_query("/lobby_update_host_state", "POST", host_state);
		return response;
	}

	async sync_watcher_player(lobby_id) {
		let payload = {
			token   : localStorage.getItem("token"),
			lobby_id: lobby_id
		};

		let response = await server_query("/lobby_get_host_state", "POST", payload);
		if (response.status == response_status.SUCESS) {
			let host_state = response.ext[0];
	
			if ( (host_state.host_time - this.player.currentTime) > 1
				|| (host_state.host_time - this.player.currentTime) < -1) {
				this.player.currentTime = host_state.host_time;
			}
			if (host_state.paused)   this.player.pause();
			if (host_state.playing)  this.player.play();
			this.player.speed = host_state.speed;
		}
		return response;
	}
};

export { Player };
