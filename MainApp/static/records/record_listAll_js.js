function deleteWarn(itemNumber, date) {
    $('#deleteRequestContainer').append('<form action = "/records/delete" method="post" id="deleteRequestInfoForm">' +
        '<input type="deleteRequestInfo" id="deleteRequestItemNumberInput" name="itemNumber">' +
        '<input type="deleteRequestInfo" id="deleteRequestDateInput" name="date"></form >');
    var c = confirm('This will delete the selected record and can\'t be recovered. Are you sure?');
    if (c == true) {
        deleteImplementation(itemNumber, date);
    }
}

function deleteImplementation(itemNumber, date) {
    document.getElementById('deleteRequestItemNumberInput').value = itemNumber;
    document.getElementById('deleteRequestDateInput').value = date;
    document.getElementById('deleteRequestInfoForm').submit();
}

function sendModifyRequest(itemNumber, date) {
    $('#modifyRequestContainer').append('<form action = "/records/modify" method="post" id="modifyRequestInfo">' +
        '<input type="modifyRequestInfo" id="modifyRequestItemNumberInput" name="itemNumber">' +
        '<input type="modifyRequestInfo" id="modifyRequestDateInput" name="date"></form >');

    document.getElementById('modifyRequestItemNumberInput').value = itemNumber;
    document.getElementById('modifyRequestDateInput').value = date;
    document.getElementById('modifyRequestInfo').submit();
}