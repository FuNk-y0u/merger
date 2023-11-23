import {
    server_query,
    response_status,
    sleep,
} from "../../utils.js"

const ipc_renderer = require('electron').ipcRenderer;

let loadingAnimationDiv = document.querySelector('#loading_animation');
let statusText = document.querySelector('#status_text');


const connect_server = async (loading_event) => {
    await sleep(1000);
    let response = await server_query('/connect',"GET",{});
    if(response.status == response_status.SUCESS)
    {
        loadingAnimationDiv.style.display = "none";
        statusText.innerHTML = "Sucessfully Connected";
        ipc_renderer.send("connect_success");
    }
    else{
        statusText.innerHTML = "Connection Error Retrying in 3 sec";
        await sleep(3000);
        location.reload();
    }
}

window.onload = connect_server;