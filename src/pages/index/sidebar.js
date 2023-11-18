// * Side bar control code
const sidebar_close = document.querySelector("#sidebar-close");
const sidebar = document.querySelector(".sidebar");

const discover_button = document.querySelector("#discover");
const join_theatre_button = document.querySelector("#join_theatre");
const comming_soon_button = document.querySelector("#comming_soon");
const settings_button = document.querySelector("#settings");
const movies = document.querySelectorAll(".show");
const iframe = document.querySelector("#iframe");

// TODO optimize side bar color changing (current one seems too heavy)
sidebar_close.addEventListener("click", () => {
    sidebar.classList.toggle("close");    
});

discover_button.addEventListener("click", () => {
    iframe.src ='../discover/discover.html';
    discover_button.querySelector(".a_page").classList.add("selected");
    join_theatre_button.querySelector(".a_page").classList.remove("selected");
    comming_soon_button.querySelector(".a_page").classList.remove("selected");
    settings_button.querySelector(".a_page").classList.remove("selected");
})

join_theatre_button.addEventListener("click", () => {
    iframe.src ='../theatre/theatre.html';
    join_theatre_button.querySelector(".a_page").classList.add("selected");
    discover_button.querySelector(".a_page").classList.remove("selected");
    comming_soon_button.querySelector(".a_page").classList.remove("selected");
    settings_button.querySelector(".a_page").classList.remove("selected");
})

comming_soon_button.addEventListener("click", () => {
    iframe.src ='../coming_soon/coming_soon.html';
    comming_soon_button.querySelector(".a_page").classList.add("selected");
    join_theatre_button.querySelector(".a_page").classList.remove("selected");
    discover_button.querySelector(".a_page").classList.remove("selected");
    settings_button.querySelector(".a_page").classList.remove("selected");
})

settings_button.addEventListener("click", () => {
    iframe.src ='../settings/settings.html';
    settings_button.querySelector(".a_page").classList.add("selected");
    join_theatre_button.querySelector(".a_page").classList.remove("selected");
    comming_soon_button.querySelector(".a_page").classList.remove("selected");
    discover_button.querySelector(".a_page").classList.remove("selected");  
})

window.onload = (event) => {
    discover_button.querySelector(".a_page").classList.add("selected");
};

