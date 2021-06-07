function setInfo() {
    var numberOfLearningGoals = $('#learningGoalsList').children().length;
    var numberOfSportsGoals = $('#sportsGoalsList').children().length;
    var numberOfLeisureGoals = $('#leisureGoalsList').children().length;

    if (numberOfLearningGoals == 0 && numberOfSportsGoals == 0 && numberOfLeisureGoals == 0) {
        $('.setGoals').append('<li class="noExistedGoal">' +
            '<h3 class="message" id="noExistedGoalMessage">There isn&apos;t any goal</h3></li>');
        $('#progress').remove();
        $('#bar').remove();
    }
    else {
        if (numberOfLearningGoals == 0) {
            $('.learningGoals').remove();
        }
        if (numberOfSportsGoals == 0) {
            $('.sportsGoals').remove();
        }
        if (numberOfLeisureGoals == 0) {
            $('.leisureGoals').remove();
        }
        var element = document.getElementById('bar');
        var percentage = parseInt(document.getElementById('bar').innerHTML);
        var width = 0;
        var id = setInterval(frame, 10);
        function frame() {
            if (width == percentage) {
                clearInterval(id);
            }
            else {
                width++;
                element.style.width = width + "%";
                element.innerHTML = width + "%";
                document.getElementById('bar').innerHTML = width + "%";
            }
        }
    }
}

function deleteWarn(goalNumber) {
    $('#deleteRequestContainer').append('<form action = "/goals/delete" method="post" id="deleteRequestInfoForm">' +
        '<input type="deleteRequestInfo" id="deleteRequestGoalNumberInput" name="goalNumber"></form>');
    var c = confirm('This will delete the selected goal and can\'t be recovered, are you sure you want to delete it?');
    if (c == true) {
        deleteImplementation(goalNumber);
    }
}

function deleteImplementation(goalNumber) {
    document.getElementById('deleteRequestGoalNumberInput').value = goalNumber;
    document.getElementById('deleteRequestInfoForm').submit();
}

function sendModifyRequest(goalNumber) {
    $('#modifyRequestContainer').append('<form action = "/goals/modify" method="post" id="modifyRequestInfo">' +
        '<input type="modifyRequestInfo" id="modifyRequestGoalNumberInput" name="goalNumber"></form>');

    document.getElementById('modifyRequestGoalNumberInput').value = goalNumber;
    document.getElementById('modifyRequestInfo').submit();
}