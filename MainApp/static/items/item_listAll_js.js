function setInfo() {
    var count = $('.setItems').children().length
    if (count == 0) {
        $('.setItems').append('<li class="noExistedItem">' +
            '<h3 class="message" id="noExistedItemMessage">There isn&apos;t any item</h3></li>');
    }
}

function deleteWarn(itemNumber) {
    $('#deleteRequestContainer').append('<form action = "/items/delete" method="post" id="deleteRequestInfoForm">' +
        '<input type="deleteRequestInfo" id="deleteRequestItemNumberInput" name="itemNumber"></form>');
    var c = confirm('This will delete its corresponding goals and records. They can\'t be recovered, are you sure you want to delete it?');
    if (c == true) {
        deleteImplementation(itemNumber);
    }
}

function deleteImplementation(itemNumber) {
    document.getElementById('deleteRequestItemNumberInput').value = itemNumber;
    document.getElementById('deleteRequestInfoForm').submit();
}

function sendModifyRequest(itemNumber) {
    $('#modifyRequestContainer').append('<form action = "/items/modify" method="post" id="modifyRequestInfo">' +
        '<input type="modifyRequestInfo" id="modifyRequestItemNumberInput" name="itemNumber"></form>');

    document.getElementById('modifyRequestItemNumberInput').value = itemNumber;
    document.getElementById('modifyRequestInfo').submit();
}