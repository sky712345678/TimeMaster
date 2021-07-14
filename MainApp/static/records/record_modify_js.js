var originalItemNumber;
var originalGoalNumber;
var originalDate;
var setDateTime;

function recordAndSetInfo() {
    originalItemNumber = document.getElementById('originalItemNumberInput').value;
    originalGoalNumber = document.getElementById('originalGoalNumberInput').value;
    originalDate = document.getElementById('dateInput').value;

    $('#setDateTimeInput').removeAttr('disabled')
    setDateTime = document.getElementById('setDateTimeInput').value;
    $('#setDateTimeInput').attr('disabled', true)

    $('#itemNumberSelect').val(originalItemNumber).change();

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
    
    $('#originalItemNumberInput').remove();
    $('#originalGoalNumberInput').remove();
    
    /*
    $('#recordInfoForm').attr('action', '/records/modify/submit')
    $('#recordInfoForm').attr('method', 'post')
    $('#recordInfoForm').removeAttr('enctype')
    */
}

$('#recordInfoForm').on('submit', function (e) {
    e.preventDefault();

    $('#originalRecordInfoContainer').append('<input type="text" id="originalItemNumberInput" name="originalItemNumber">');
    $('#originalRecordInfoContainer').append('<input type="text" id="originalGoalNumberInput" name="originalGoalNumber">');
    $('#originalRecordInfoContainer').append('<input type="text" id="originalDateInput" name="originalDate">');

    document.getElementById('originalItemNumberInput').value = originalItemNumber;
    document.getElementById('originalGoalNumberInput').value = originalGoalNumber;
    document.getElementById('originalDateInput').value = originalDate;

    var form = $('#recordInfoForm')[0];
    var formData = new FormData(form);

    $.ajax({
        url: '/records/modify/check',
        type: 'POST',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            if (data == 'Y') {
                $('#setDateTimeInput').removeAttr('disabled');
                document.getElementById("recordInfoForm").submit();
            }
            else {
                window.alert(data);
                $('#originalItemNumberInput').remove();
                $('#originalGoalNumberInput').remove();
                $('#originalDateInput').remove();
            }
        },
        error: function () {
            window.alert('Ajax error occured')
        }
    })
})

$('#cancelButton').click(function (e) {
    window.location.href = "/records/listAll";
})

function ajax_getAvailableGoals() {
    var form = $('#recordInfoForm')[0];
    var formData = new FormData(form);

    $.ajax({
        url: '/records/modify/getAvailableGoals',
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
                if (originalGoalNumber == data[i].GoalNumber) {
                    $('#goalNumberSelect').val(data[i].GoalNumber).change();
                }
            }
        },
        error: function () {
            window.alert('Ajax error occured');
        }
    })
}

$('#itemNumberSelect').change(function () {
    $('#achievePercentageContainer').attr('style', 'display: none;');
    
    ajax_getAvailableGoals();
})

$('#dateInput').change(function () {
    ajax_getAvailableGoals();
})

$('#goalNumberSelect').change(function () {
    if (document.getElementById('goalNumberSelect').value != '') {
        var form = $('#recordInfoForm')[0];
        var formData = new FormData(form);

        $.ajax({
            url: '/goals/get_percentage',
            type: 'POST',
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                document.getElementById('achievePercentageInput').value = data;
            },
            error: function () {
                window.alert('Ajax error occured');
            }
        })
        
        $('#achievePercentageContainer').removeAttr('style');
    }
    else {
        $('#achievePercentageContainer').attr('style', 'display: none;');
    }
})