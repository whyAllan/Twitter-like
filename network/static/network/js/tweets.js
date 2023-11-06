function like(x) {
    // Change the color of the like button
  if (x.style.color === "blue") {
      x.style.color = "black";
  } else {
      x.style.color = "blue";   
}
}


// Show the edit form
document.querySelectorAll("#edit_post").forEach((element) => {

    element.addEventListener("click", () => {
        const button = element.dataset.post;
        post = document.querySelector(`#post${button}`);
        content = post.innerHTML;
        post.style.display = "none";
        form = document.querySelector(`#form${button}`);
        form.innerHTML = `<textarea name="content" style="width: 100%; height: 100px;">${content}</textarea><br><button type="submit" id="save_post" class="btn btn-outline-success">Save</button> `;
        cancel_button = document.createElement("button");
        cancel_button.className = "btn btn-outline-danger";
        cancel_button.innerHTML = "Cancel";
        form.append(cancel_button);
        form.style.display = "block";
        // If the user sends the form, display the post
        document.addEventListener("submit", (event) => {
            form.style.display = "none";
            post.style.display = "block";
        })
         // If the user cancels the edit, display the post
        cancel_button.addEventListener("click", (event) => {
            event.preventDefault();
            form.style.display = "none";
            post.style.display = "block";
        })
        // Let the user send the form with Enter
        document.addEventListener("keydown", (event) => {
            if (event.keyCode =='13') {
                event.preventDefault();
                document.querySelector("#save_post").click();
            }
        })
    })});

 // delete posts on the replyes page
function Delete() {
    conmation = window.confirm("Are you sure you want to delete this post?");
    
    if (conmation == true) {
        document.querySelector("#delete_form").submit();
    }
}

// Load followers or followings
function Load(x) {
    f = x.dataset.load
    console.log(f)
    
}