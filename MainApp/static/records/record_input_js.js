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
                    $('#goalNumberSelect').append($('<option></option>').attr('value', data[i].GoalNumber).text(data[i].Goal));
                }
                var today = new Date();
                var dd = today.getDate();
                var mm = today.getMonth()+1; //January is 0!
                var yyyy = today.getFullYear();

                if(dd<10){
                    dd='0'+dd
                } 
                if(mm<10){
                    mm='0'+mm
                } 

                today = yyyy+'-'+mm+'-'+dd;
                document.getElementById("dateInput").setAttribute("max", today);
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

$('#itemNumberSelect').change(function () {
    $('#achievePercentageContainer').attr('style', 'display: none;');
    
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

$('#goalNumberSelect').change(function () {
    if (document.getElementById('goalNumberSelect').value != '') {
        $('#achievePercentageContainer').removeAttr('style');
    }
    else {
        $('#achievePercentageContainer').attr('style', 'display: none;');
    }
})