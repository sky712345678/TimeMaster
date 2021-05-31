function categoryCheck(that) {
    if (that.value != "Learning") {
        document.getElementById("itemNumberContainer").style.display = "none";
        document.getElementById("nameInput").placeholder = "Please enter item name"
    }
    else {
        document.getElementById("itemNumberContainer").style.display = "block";
        document.getElementById("nameInput").placeholder = "Please enter course name"
    }
}