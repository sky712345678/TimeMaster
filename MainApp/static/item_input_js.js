function categoryCheck(that) {
    if (that.value != "Learning") {
        document.getElementById("serialNumberContainer").style.display = "none";
    }
    else {
        document.getElementById("serialNumberContainer").style.display = "block";
    }
}