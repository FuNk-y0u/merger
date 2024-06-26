const {app, BrowserWindow, ipcMain} = require('electron');
const EventEmitter = require('events');
const event_main = new EventEmitter();



const create_window = () =>{
    const window = new BrowserWindow({
        width: 854,
        height: 480,
        "minHeight": 630,
        "minWidth": 1130,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            devTools: true,
        }
    });
    //disables menu
	window.setMenu(null);
    window.loadFile(`src/pages/loading_page/loading_page.html`);

    event_main.on('connect_success', () => {
        window.loadFile(`src/pages/init.html`);
    });

    event_main.on('logout',() => {
        window.loadFile(`src/pages/login/login.html`);
    })
}

app.whenReady().then(create_window);

ipcMain.on('connect_success', (event) => {
    setTimeout(() => event_main.emit('connect_success'), 1000);
});

ipcMain.on('logout', (event) => {
    event_main.emit('logout');
})
