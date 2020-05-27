function displaySearchHeader() {
    if (counter === 0) {
        document.getElementById('navbarHeader').style.display = "";
    }
    counter = ++counter;
    if (counter % 2) {
        body.classList.remove("hide-search");
        body.classList.add("show-search");
    } else {
        body.classList.remove("show-search");
        body.classList.add("hide-search");
    }
}
