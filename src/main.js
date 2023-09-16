const { app, BrowserWindow } = require('electron')

app.whenReady().then(
    () => {
        const window = new BrowserWindow(
            {
                width: 854,
                height: 480,
                webPreferences: {
                    nodeIntegration: true
                },
                
            }
        );

        window.loadFile('html/index.html');
    }
)