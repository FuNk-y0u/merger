import {
	server_ip,
	server_query,
	response_status,
	redirect_page,
	loose_redirect
} from "../../utils.js"

let emailInput = document.querySelector("#email_input");
let passwordInput = document.querySelector("#password_input");
let rePasswordInput = document.querySelector("#re_password_input");
let usernameInput = document.querySelector("#username_input");
let submitButton = document.querySelector('#submit');
let errorText = document.querySelector('#error_text');

function check_password(inputtxt) 
{ 
    var passw =  /^[A-Za-z]\w{7,14}$/;
    if(inputtxt.match(passw)) 
    { 
        return true;
    }
    else
    { 
        return false;
    }
}

function validate_email(inputText)
{
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if(inputText.match(mailformat))
    {
        return true;
    }
    else
    {
        return false;
    }
}

function validate_username(inputText)
{
    var username = /^[0-9A-Za-z]{3,16}$/;
    if(inputText.match(username))
    {
        return true;
    }
    else
    {
        return false;
    }
}



submitButton.addEventListener('click', async () => {
    let email = emailInput.value;
    let password = passwordInput.value;
    let rePassword = rePasswordInput.value;
    let username = usernameInput.value;
    if(email == "" || password == "" || rePassword == ""){
        errorText.innerHTML = "You missed something(s)!";
        return;
    }
    else if(!validate_email(email)){
        errorText.innerHTML = "Invalid email mate!";
        return;
    }
    else if(password != rePassword){
        errorText.innerHTML = "Passwords doesnt match bro!";
        return;
    }
    else if(!check_password(password)){
        errorText.innerHTML = "Password must be between 7 - 16 characters long and only characters, numeric digits, underscore and first character must be a letter";
        return;
    }
    else if(!validate_username(username)){
        errorText.innerHTML = "Username must be between length 3 to 16 and must only contain letters from A to Z and numbers from 0 to 9";

    }
    else{
        let payload = {
            email: email,
            username: username,
            password: password
        }
        let response = await server_query('/signup',"POST", payload, false);
        if(response.status == response_status.FAILED){
            errorText.innerHTML = response.log;
            return;
        }
        loose_redirect('email_verify');
    }
})


