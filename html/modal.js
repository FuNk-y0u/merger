
class Modal {
	constructor(root) {
		this.id = "info-box";
		this.root = root;

		this.append_modal();
		this.b_modal_ele = document.getElementById(this.id);
		this.b_modal = new bootstrap.Modal(this.b_modal_ele);
	}

	show() {
		this.b_modal.show();
	}

	set_title(title) {
		let modal_title = this.b_modal_ele
			.querySelector(".modal-title");
		modal_title.textContent = title;
	}

	set_body(body) {
		let modal_body = this.b_modal_ele
			.querySelector(".modal-body")
			.firstChild;
		modal_body.innerHTML = body;
	}

	append_modal() {
		// Modal element
		let modal = document.createElement("div");
		modal.setAttribute("id", this.id);
		modal.setAttribute("class", "modal fade");
		modal.setAttribute("role", "dialog");

		// Modal dialog
		let modal_dialog = document.createElement("div");
		modal_dialog.setAttribute("class", "modal-dialog");

		// Modal contents
		let modal_content = document.createElement("div");
		modal_content.setAttribute("class", "modal-content");

		// Modal header
		let modal_header = document.createElement("div");
		modal_header.setAttribute("class", "modal-header");

		let modal_title = document.createElement("h4");
		modal_title.setAttribute("class", "modal-title");
		modal_title.innerHTML = "Title";

		modal_header.appendChild(modal_title);

		// Modal body
		let modal_body = document.createElement("div");
		modal_body.setAttribute("class", "modal-body");

		let body = document.createElement("p");
		body.innerHTML = "Body";

		modal_body.appendChild(body);

		// Modal footer
		let modal_footer = document.createElement("div");
		modal_footer.setAttribute("class", "modal-footer");

		let close_button = document.createElement("button");
		close_button.setAttribute("class", "btn btn-default");
		close_button.setAttribute("data-bs-dismiss", "modal");
		close_button.innerHTML = "Close";

		modal_footer.appendChild(close_button);

		// Appending to modal
		modal_content.appendChild(modal_header);
		modal_content.appendChild(modal_body);
		modal_content.appendChild(modal_footer);

		modal_dialog.appendChild(modal_content);
		modal.appendChild(modal_dialog);

		// Appending to root
		this.root.appendChild(modal);
	}
};

export { Modal };
