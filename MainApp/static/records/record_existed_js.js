function back() {
    window.history.back();
}

function sendModifyRequest(itemNumber, date) {
    $('#modifyRequestContainer').append('<form action = "/records/modify" method="post" id="modifyRequestInfo">' +
        '<input type="modifyRequestInfo" id="modifyRequestItemNumberInput" name="itemNumber">' +
        '<input type="modifyRequestInfo" id="modifyRequestDateInput" name="date"></form >');

    document.getElementById('modifyRequestItemNumberInput').value = itemNumber;
    document.getElementById('modifyRequestDateInput').value = date;
    document.getElementById('modifyRequestInfo').submit();
}