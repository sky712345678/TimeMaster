function deleteWarn(itemNumber) {
    $('#deleteRequestContainer').append('<form action = "/items/delete" method="post" id="deleteRequestInfoForm">' +
        '<input type="deleteRequestInfo" id="deleteRequestItemNumberInput" name="itemNumber"></form>')
    var c = confirm('This will delete its corresponding goals and records. They can\'t be recovered, are you sure you want to delete it?')
    if (c == true) {
        deleteImplementation(itemNumber)
    }
}

function deleteImplementation(itemNumber) {
    document.getElementById('deleteRequestItemNumberInput').value = itemNumber
    document.getElementById('deleteRequestInfoForm').submit()
}

function sendModifyRequest(itemNumber) {
    $('#modifyRequestContainer').append('<form action = "/items/modify" method="post" id="modifyRequestInfo">' +
        '<input type="modifyRequestInfo" id="modifyRequestItemNumberInput" name="itemNumber"></form>')

    document.getElementById('modifyRequestItemNumberInput').value = itemNumber
    document.getElementById('modifyRequestInfo').submit()
}