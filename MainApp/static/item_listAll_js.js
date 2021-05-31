function deleteWarn(itemNumber) {
    $('#deleteRequestContainer').append('<form action = "/items/delete" method="post" id="deleteRequestInfo">' +
                                       '<input type="deleteRequestInfo" id="deleteRequestItemNumber" name="itemNumber"></form>')
    var c = confirm("This will delete its corresponding goals and records, are you sure?")
    if (c == true) {
        deleteImplementation(itemNumber)
    }
}

function deleteImplementation(itemNumber) {
    document.getElementById("deleteRequestItemNumber").value = itemNumber
    document.getElementById("deleteRequestInfo").submit()
}