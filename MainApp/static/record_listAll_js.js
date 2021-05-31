function deleteWarn(itemNumber, date) {
    $('#deleteRequestContainer').append('<form action = "/records/delete" method="post" id="deleteRequestInfo">' +
        '<input type="deleteRequestInfo" id="deleteRequestItemNumber" name="itemNumber">' +
        '<input type="deleteRequestInfo" id="deleteRequestDate" name="date"></form > ')
    var c = confirm("This will delete its corresponding goals and records, are you sure?")
    if (c == true) {
        deleteImplementation(itemNumber, date)
    }
}

function deleteImplementation(itemNumber, date) {
    document.getElementById("deleteRequestItemNumber").value = itemNumber
    document.getElementById("deleteRequestDate").value = date
    document.getElementById("deleteRequestInfo").submit()
}