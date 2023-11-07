// Change follow button color
document.getElementsByName('follow').forEach(button => button.addEventListener("click", function() {
    if (this.classList.contains("btn-outline-success")) {
        this.classList.remove("btn-outline-success");
        this.classList.add("btn-outline-danger");
        // the values are swapped cause of htmx behavior
        this.value = "follow";
        this.innerHTML = "unfollow";
    } else {
        this.classList.remove("btn-outline-danger");
        this.classList.add("btn-outline-success");
        this.value = "unfollow";
        this.innerHTML = "follow";
    }
}))