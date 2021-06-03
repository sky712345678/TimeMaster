function categoryCheck(that) {
    if (that.value != "Learning") {
        document.getElementById("itemNumberContainer").style.display = "none";
        document.getElementById("nameInput").placeholder = "Please enter item name";
    }
    else {
        document.getElementById("itemNumberContainer").style.display = "block";
        document.getElementById("nameInput").placeholder = "Please enter course name";
    }
}

$('#submitButton').click(function (e) {
    e.preventDefault();
    var form = $('#itemInfo')[0];
    var formData = new FormData(form);
    $.ajax({
        url: '/items/input/submit',
        type: 'POST',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            window.alert(data)
        },
        error: function () {
            window.alert('error occured')
        }
    })
})