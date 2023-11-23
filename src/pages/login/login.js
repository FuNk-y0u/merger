import {
	server_ip,
	server_query,
	response_status,
	redirect_page,
	loose_redirect
} from "../../utils.js"

let emailInput = document.querySelector('#email_input');
let passwordInput = document.querySelector('#password_input');
let submitButton = document.querySelector('#submit');
let errorText = document.querySelector('#error_text');

submitButton.addEventListener("click", async () => {
    if(emailInput.value == "" || passwordInput.value == "")
    {
        errorText.innerHTML = "Woops! you missed your email or password";
    }
    else{

        let payload = {
            email: emailInput.value,
            password: passwordInput.value
        };

        let response = await server_query("/login", "POST", payload);
        if(response.status != response_status.SUCESS){
            console.log(response.log);
            errorText.innerHTML = response.log;
            return;
        }

        let token = response.ext[0].token;
        localStorage.setItem("token",token);

        redirect_page("index");
    }
})