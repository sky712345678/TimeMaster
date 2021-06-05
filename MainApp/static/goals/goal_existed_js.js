function back() {
    window.history.back();
}

function sendModifyRequest(goalNumber) {
    $('#modifyRequestContainer').append('<form action = "/goals/modify" method="post" id="modifyRequestInfo">' +
        '<input type="modifyRequestInfo" id="modifyRequestGoalNumberInput" name="goalNumber"></form>');

    document.getElementById('modifyRequestGoalNumberInput').value = goalNumber;
    document.getElementById('modifyRequestInfo').submit();
}