import {
	server_ip,
	server_query,
	response_status,
	redirect_page,
	loose_redirect
} from "../../utils/utils.js"

const ipcRenderer = require('electron').ipcRenderer;

/*
 * Send connection ping and change ui
 */
const connect_server  = async (loadingEvent) => {
    let retryCount = 0;
    let response = await server_query("/connect","GET",{});
    if (response.status != response_status.SUCESS)
    {
        
        document.getElementById("title").style.display = 'none';
        document.getElementById("loading_animation").style.display = 'none';
        document.getElementById("error_h1").innerHTML = `connection error to merger servers, please check your network or try again`;
    }
    else{

        document.getElementById("title").innerHTML = `Succeed!`;
        ipcRenderer.send("connection_success");        
    }
}

window.addEventListener("load", function() {

    connect_server();
});