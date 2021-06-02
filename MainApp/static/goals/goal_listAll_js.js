function deleteWarn(goalNumber) {
    $('#deleteRequestContainer').append('<form action = "/goals/delete" method="post" id="deleteRequestInfo">' +
        '<input type="deleteRequestInfo" id="deleteRequestGoalNumber" name="goalNumber"></form>')
    var c = confirm("This will delete the selected goal and can't be recovered. Are you sure?")
    if (c == true) {
        deleteImplementation(goalNumber)
    }
}

function deleteImplementation(goalNumber) {
    document.getElementById("deleteRequestGoalNumber").value = goalNumber
    document.getElementById("deleteRequestInfo").submit()
}