function deleteWarn(goalNumber) {
    $('#deleteRequestContainer').append('<form action = "/goals/delete" method="post" id="deleteRequestInfoForm">' +
        '<input type="deleteRequestInfo" id="deleteRequestGoalNumberInput" name="goalNumber"></form>')
    var c = confirm('This will delete the selected goal and can\'t be recovered. Are you sure?')
    if (c == true) {
        deleteImplementation(goalNumber)
    }
}

function deleteImplementation(goalNumber) {
    document.getElementById('deleteRequestGoalNumberInput').value = goalNumber
    document.getElementById('deleteRequestInfoForm').submit()
}