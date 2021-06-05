function setInfo() {
    var count = $('.setGoals').children().length
    if (count == 0) {
        $('.setGoals').append('<li class="noExistedGoal">' +
            '<h3 class="message" id="noExistedGoalMessage">There isn&apos;t any goal</h3></li>');
    }
}

function deleteWarn(goalNumber) {
    $('#deleteRequestContainer').append('<form action = "/goals/delete" method="post" id="deleteRequestInfoForm">' +
        '<input type="deleteRequestInfo" id="deleteRequestGoalNumberInput" name="goalNumber"></form>');
    var c = confirm('This will delete the selected goal and can\'t be recovered, are you sure you want to delete it?');
    if (c == true) {
        deleteImplementation(goalNumber);
    }
}

function deleteImplementation(goalNumber) {
    document.getElementById('deleteRequestGoalNumberInput').value = goalNumber;
    document.getElementById('deleteRequestInfoForm').submit();
}

function sendModifyRequest(goalNumber) {
    $('#modifyRequestContainer').append('<form action = "/goals/modify" method="post" id="modifyRequestInfo">' +
        '<input type="modifyRequestInfo" id="modifyRequestGoalNumberInput" name="goalNumber"></form>');

    document.getElementById('modifyRequestGoalNumberInput').value = goalNumber;
    document.getElementById('modifyRequestInfo').submit();
}