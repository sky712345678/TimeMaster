function setInfo() {
    var count = $('#itemNumberSelect').children().length;

    if (count > 0) {
        var form = $('#recordInfoForm')[0];
        var formData = new FormData(form);

        $.ajax({
            url: '/records/input/getAvailableGoals',
            type: 'POST',
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                $('#goalNumberSelect').empty();
                $('#goalNumberSelect').append('<option value="">none</option>');
                for (var i = 0; i < data.length; i++) {
                    console.log(data[i])
                    $('#goalNumberSelect').append($('<option></option>').attr('value', data[i].GoalNumber).text(data[i].Goal));
                }
            },
            error: function () {
                window.alert('Ajax error occured');
            }
        });
    }
    else {
        $('#title').text('Please add an item first!')
        $('#itemNumberSelect').attr('disabled', true);
        $('#dateInput').attr('disabled', true);
        $('#durationInput').attr('disabled', true);
        $('#goalNumberSelect').attr('disabled', true);
        $('#achievePercentageInput').attr('disabled', true);
        $('#descriptionInput').attr('disabled', true);
        $('#submitButton').attr('disabled', true);

        window.alert('Please add an item first!');
    }
}

/*
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
*/

$('#itemNumberSelect').change(function () {
    var form = $('#recordInfoForm')[0];
    var formData = new FormData(form);

    $.ajax({
        url: '/records/input/getAvailableGoals',
        type: 'POST',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            $('#goalNumberSelect').empty();
            $('#goalNumberSelect').append('<option value="">none</option>');
            for (var i = 0; i < data.length; i++){
                $('#goalNumberSelect').append($('<option></option>').attr('value', data[i].GoalNumber).text(data[i].Goal));
            }
        },
        error: function () {
            window.alert('Ajax error occured');
        }
    })
})