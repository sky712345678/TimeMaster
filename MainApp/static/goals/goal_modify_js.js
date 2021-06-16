var originalItemNumber;
var originalGoal;
var goalNumberBackup;

function recordAndSetInfo() {
    originalItemNumber = document.getElementById('originalItemNumberInput').value;
    originalGoal = document.getElementById('goalInput').value;
    goalNumberBackup = document.getElementById("goalNumberInput").value;

    /*
    $('#goalNumberInput').removeAttr('disabled')

    var form = $('#goalInfoForm')[0];
    var formData = new FormData(form);

    $.ajax({
        url: '/goals/modify/getInfo',
        type: 'POST',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            $('#itemNumberSelect').val(data.itemNumber).change();
            $('#achievedSelect').val(data.achieved).change();
        },
        error: function () {
            window.alert('Ajax error occured')
        }
    })
    */
    
    $('#itemNumberSelect').val(document.getElementById('originalItemNumberInput').value).change();
    $('#achievedSelect').val(document.getElementById('originalAchievedInput').value).change();

    /*
    $('#goalInfoForm').attr('action', '/goals/modify/submit')
    $('#goalInfoForm').attr('method', 'post')
    $('#goalInfoForm').removeAttr('enctype')
    $('#goalNumberInput').attr('disabled', true)
    */
    
    $('#originalItemNumberInput').remove();
    $('#originalAchievedInput').remove();
}

$('#goalInfoForm').on('submit', function (e) {
    e.preventDefault();

    $('#originalGoalInfoContainer').append('<input type="text" id="originalItemNumberInput" name="originalItemNumber">');
    $('#originalGoalInfoContainer').append('<input type="text" id="originalGoalInput" name="originalGoal">');

    document.getElementById('originalItemNumberInput').value = originalItemNumber;
    document.getElementById('originalGoalInput').value = originalGoal;

    var form = $('#goalInfoForm')[0];
    var formData = new FormData(form);

    $.ajax({
        url: '/goals/modify/check',
        type: 'POST',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            if (data == 'Y') {
                $('#goalNumberInput').removeAttr('disabled');

                document.getElementById('goalNumberInput').value = goalNumberBackup;

                document.getElementById('goalInfoForm').submit();
            }
            else {
                window.alert(data);
                $('#originalItemNumberInput').remove();
                $('#originalGoalInput').remove();
            }
        },
        error: function () {
            window.alert('Ajax error occured')
        }
    })
})

$('#cancelButton').click(function (e) {
    window.location.href = "/goals/listAll";
})