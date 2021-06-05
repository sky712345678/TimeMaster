var originalItemNumber;
var originalDate;
var originalGoalNumber;

function recordAndSetInfo() {
    originalItemNumber = document.getElementById('originalItemNumberInput').value;
    originalDate = document.getElementById('dateInput').value;
    originalGoalNumber = document.getElementById('originalGoalNumberInput').value;

    $('#itemNumberSelect').val(originalItemNumber).change();

    $('#originalItemNumberInput').remove();
    $('#originalGoalNumberInput').remove();

    /*
    $('#recordInfoForm').attr('action', '/records/modify/submit')
    $('#recordInfoForm').attr('method', 'post')
    $('#recordInfoForm').removeAttr('enctype')
    */
}

$('#confirmButton').click(function (e) {
    e.preventDefault();

    $('#recordInfoForm').append('<div id="originalRecordInfoContainer" style="display: none;">');

    $('#originalRecordInfoContainer').append('<input type="record" id="originalItemNumberInput" name="originalItemNumber"></form>');
    $('#originalRecordInfoContainer').append('<input type="record" id="originalDate" name="originalDate"></form>');

    document.getElementById('originalItemNumberInput').value = originalItemNumber;
    document.getElementById('originalDate').value = originalDate;

    document.getElementById("recordInfoForm").submit();
})

$('#cancelButton').click(function (e) {
    window.location.href = "/records/listAll";
})

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
            $('#goalNumberSelect').append('<option value="">None</option>');
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
})