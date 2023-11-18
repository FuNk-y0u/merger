
// * Hover Movie Control Code
let is_hovering = false;
let prev_interval = null;

let on_hover = (id) => {
    if(prev_interval != null){
        clearInterval(prev_interval);
        is_hovering = true;
        prev_interval = setInterval(display_eager,1000,id);
    }
    else{
        is_hovering = true;
        prev_interval = setInterval(display_eager,1000,id);
    }
}

let on_leave =  (id) => {
    is_hovering = false;
    document.getElementById(id).classList.remove("eager");
    document.getElementById(id).getElementsByClassName("eager_div")[0].style.display = 'none';
    document.getElementById(id).getElementsByClassName("non_eager_div")[0].style.display = 'block';
}

let display_eager = (id) => {
    if(is_hovering){
        document.getElementById(id).classList.add("eager");
        document.getElementById(id).getElementsByClassName("eager_div")[0].style.display = 'block';
        document.getElementById(id).getElementsByClassName("non_eager_div")[0].style.display = 'none';
    }
}

