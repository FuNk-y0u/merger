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
				nodeIntegration: true
			},
		});
	
		window.loadFile(`src/index.html`);
	
		let app_path = "file://" + app.getAppPath() + "/src";
	
		window.webContents
			.executeJavaScript(`localStorage.clear();`, true)
			.catch(error => {
				console.log(error);
			});
	
		window.webContents
			.executeJavaScript(`localStorage.setItem("root_path", "${app_path}");`, true)
			.catch(error => {
				console.log(error);
			});
	});
