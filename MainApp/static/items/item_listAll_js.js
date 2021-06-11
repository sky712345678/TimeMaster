function setInfo() {
    var numberOfLearningItems = $('#learningItemsContainer div').length;
    var numberOfSportsItems = $('#sportsItemsContainer div').length;
    var numberOfLeisureItems = $('#leisureItemsContainer div').length;

    if (numberOfLearningItems == 0) {
        $('.learningItems').remove();
    }
    if (numberOfSportsItems == 0) {
        $('.sportsItems').remove();
    }
    if (numberOfLeisureItems == 0) {
        $('.leisureItems').remove();
    }

    if (numberOfLearningItems == 0 && numberOfSportsItems == 0 && numberOfLeisureItems == 0) {
        $('#itemContainer').append('<h3 class="message">There isn&apos;t any item</h3></li>');
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