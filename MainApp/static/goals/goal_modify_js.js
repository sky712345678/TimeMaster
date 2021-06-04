var goalNumberBackup

function recordAndSetInfo() {
    goalNumberBackup = document.getElementById("goalNumberInput").value

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

    console.log(document.getElementById('originalItemNumberInput').value)

    /*
    $('#goalInfoForm').attr('action', '/goals/modify/submit')
    $('#goalInfoForm').attr('method', 'post')
    $('#goalInfoForm').removeAttr('enctype')
    $('#goalNumberInput').attr('disabled', true)
    */
    
    $('#originalItemNumberInput').remove()
    $('#originalAchievedInput').remove()
}

$('#confirmButton').click(function (e) {
    e.preventDefault();

    $('#goalNumberInput').removeAttr('disabled');

    document.getElementById("goalNumberInput").value = goalNumberBackup;

    document.getElementById("goalInfoForm").submit();
})

$('#cancelButton').click(function (e) {
    window.location.href = "/goals/listAll";
})