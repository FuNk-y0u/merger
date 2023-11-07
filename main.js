const {app,BrowserWindow, ipcMain} = require("electron");
const EventEmitter = require('events');
const loadingEvent = new EventEmitter();
let source = null;
function createWindow () {
	const window = new BrowserWindow({
		width: 854,
		height: 480,
		"minHeight": 480,
		"minWidth": 854,
		webPreferences: {
			nodeIntegration: true,
			contextIsolation: false,
			devTools: true,
		},
	})

	// disables menu
	window.setMenu(null);

	window.loadFile(`src/pages/connect_loading/loading.html`);
	loadingEvent.on(`success`, () => {
		window.loadFile(`src/index.html`)
	})
}

app.whenReady().then(() => {
		createWindow()
		app.on(`activate`, () => {
			if(BrowserWindow.getAllWindows().length === 0){
				createWindow()
			}
		});
});

app.on(`window-all-closed`, () => {
	if(process.platform !== `darwin`)
	{
		app.quit()
	}
})

ipcMain.on('connection_success', (event)=> {
	setTimeout(() => {loadingEvent.emit(`success`)},1000);
})

ipcMain.on('add_source', (event,source) => {
	source = source;
});

ipcMain.on('get_source', (event)=> {
	return source;
})

