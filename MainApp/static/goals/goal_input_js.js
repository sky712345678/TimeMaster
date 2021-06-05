function setInfo() {
    var count = $('#itemNumberSelect').children().length;

    if (count == 0) {
        $('#title').text('Please add an item first!')
        $('#itemNumberSelect').attr('disabled', true);
        $('#goalInput').attr('disabled', true);
        $('#submitButton').attr('disabled', true);

        window.alert('Please add an item first!');
    }
}

/*
$('#submitButton').click(function (e) {
    e.preventDefault();

    var form = $('#goalInfoForm')[0];
    var formData = new FormData(form);

    $.ajax({
        url: '/goals/input/submit',
        type: 'POST',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            window.alert(data)
        },
        error: function () {
            window.alert('Ajax error occured')
        }
    })
})
*/