$('#submitButton').click(function (e) {
    e.preventDefault();
    var form = $('#recordInfoForm')[0];
    var formData = new FormData(form);
    $.ajax({
        url: '/records/input/submit',
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