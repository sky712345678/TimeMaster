function setInfo() {
    var count = $('.allRecords').children().length
    if (count == 0) {
        $('#recordListContainer').append('<h3 class="message" id="noExistedRecordMessage">There isn&apos;t any record</h3>');
    }
}

function deleteWarn(itemNumber, date, setDateTime) {
    $('#deleteRequestContainer').append('<form action = "/records/delete" method="post" id="deleteRequestInfoForm">' +
        '<input type="text" id="deleteRequestItemNumberInput" name="itemNumber">' +
        '<input type="text" id="deleteRequestDateInput" name="date">' +
        '<input type="text" id="deleteRequestSetDateTimeInput" name="setDateTime"></form >');
    var c = confirm('This will delete the selected record and can\'t be recovered, are you sure you want to delete it?');
    if (c == true) {
        deleteImplementation(itemNumber, date, setDateTime);
    }
}

function deleteImplementation(itemNumber, date, setDateTime) {
    document.getElementById('deleteRequestItemNumberInput').value = itemNumber;
    document.getElementById('deleteRequestDateInput').value = date;
    document.getElementById('deleteRequestSetDateTimeInput').value = setDateTime;
    document.getElementById('deleteRequestInfoForm').submit();
}

function sendModifyRequest(itemNumber, date, setDateTime) {
    $('#modifyRequestContainer').append('<form action = "/records/modify" method="post" id="modifyRequestInfo">' +
        '<input type="text" id="modifyRequestItemNumberInput" name="itemNumber">' +
        '<input type="text" id="modifyRequestDateInput" name="date">' +
        '<input type="text" id="modifyRequestSetDateTimeInput" name="setDateTime"></form >');

    document.getElementById('modifyRequestItemNumberInput').value = itemNumber;
    document.getElementById('modifyRequestDateInput').value = date;
    document.getElementById('modifyRequestSetDateTimeInput').value = setDateTime;
    document.getElementById('modifyRequestInfo').submit();
}