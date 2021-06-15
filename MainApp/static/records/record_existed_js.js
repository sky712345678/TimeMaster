function back() {
    window.history.back();
}

function sendModifyRequest(itemNumber, dateTime) {
    $('#modifyRequestContainer').append('<form action = "/records/modify" method="post" id="modifyRequestInfo">' +
        '<input type="text" id="modifyRequestItemNumberInput" name="itemNumber">' +
        '<input type="text" id="modifyRequestDateTimeInput" name="setDateTime"></form >');

    document.getElementById('modifyRequestItemNumberInput').value = itemNumber;
    document.getElementById('modifyRequestDateTimeInput').value = dateTime;
    document.getElementById('modifyRequestInfo').submit();
}