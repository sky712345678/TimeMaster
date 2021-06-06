function categoryCheck(that) {
    if (that.value != 'Learning') {
        $('#itemNumberInput').attr('disabled', true);
        document.getElementById('itemNumberContainer').style.display = 'none';
        document.getElementById('nameInput').placeholder = 'Please enter item name';
    }
    else {
        $('#itemNumberInput').removeAttr('disabled');
        document.getElementById('itemNumberContainer').style.display = 'block';
        document.getElementById('nameInput').placeholder = 'Please enter course name';
    }
}


$('#submitButton').click(function (e) {
    e.preventDefault();

    $('#itemNumberInput').removeAttr('disabled');

    var form = $('#itemInfoForm')[0];
    var formData = new FormData(form);
    
    $.ajax({
        url: '/items/input/check',
        type: 'POST',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            if (data == 'Y') {
                document.getElementById('itemInfoForm').submit();
            }
            else {
                window.alert(data);
            }
        },
        error: function () {
            window.alert('Ajax error occured');
        }
    })
})
