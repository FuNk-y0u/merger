const {
	app,
	BrowserWindow
} = require("electron");

app
	.whenReady()
	.then(() => {
		const window = new BrowserWindow({
			width: 854,
			height: 480,
			"minHeight": 480,
			"minWidth": 854,
			webPreferences: {
				nodeIntegration: true,
				contextIsolation: false
			},
		});
	
		window.loadFile(`src/index.html`);
	});
