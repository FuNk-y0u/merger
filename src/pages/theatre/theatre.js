import { Modal } from "../../static/js/modal.js";
const modal = new Modal(
	document.getElementById("modal_root")
);

window.onload = () =>{
    modal.set_title("Join theatre");
    modal.set_body(`
    <div class="form-group p-5">
    <label for="exampleInputEmail1">Theatre Code</label>
    <input type="text" class="form-control" id="" placeholder="xxxx-xxxx-xxxx-xxxx">
    <button type="button" class="btn btn-primary">Join + </button>
    </div>
    
    `);
    modal.show();
}