function back() {
    window.history.back();
}

function sendModifyRequest(itemNumber, date, time) {
    $('#modifyRequestContainer').append('<form action = "/records/modify" method="post" id="modifyRequestInfo">' +
        '<input type="modifyRequestInfo" id="modifyRequestItemNumberInput" name="itemNumber">' +
        '<input type="modifyRequestInfo" id="modifyRequestDateInput" name="date">' +
        '<input type="modifyRequestInfo" id="modifyRequestTimeInput" name="time"></form >');

    document.getElementById('modifyRequestItemNumberInput').value = itemNumber;
    document.getElementById('modifyRequestDateInput').value = date;
    document.getElementById('modifyRequestTimeInput').value = time;
    document.getElementById('modifyRequestInfo').submit();
}