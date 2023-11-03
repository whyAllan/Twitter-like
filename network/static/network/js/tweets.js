function like(x) {
    // Change the color and count of likes
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
        post = document.querySelector(`#${button}`);
        post.style.display = "none";
    })});
