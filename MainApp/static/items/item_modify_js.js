var originalItemNumber;

function categoryCheck(that) {
    if (that.value != 'Learning') {
        document.getElementById('itemNumberContainer').style.display = 'none';
        document.getElementById('nameInput').placeholder = 'Please enter item name';
    }
    else {
        document.getElementById('itemNumberContainer').style.display = 'block';
        document.getElementById('nameInput').placeholder = 'Please enter course name';
    }
}

function recordAndSetInfo() {
    originalItemNumber = document.getElementById("itemNumberInput").value;

    /*
    var form = $('#itemInfoForm')[0];
    var formData = new FormData(form);
    $.ajax({
        url: '/items/modify/getInfo',
        type: 'POST',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            $('#categorySelect').val(data).change();
        },
        error: function () {
            window.alert('Ajax error occured')
        }
    })
    */
    
    $('#categorySelect').val(document.getElementById('originalCategoryInput').value).change();

    $('#originalCategoryInput').remove();

    /*
    $('#itemInfoForm').attr('action', '/items/modify/submit')
    $('#itemInfoForm').attr('method', 'post')
    $('#itemInfoForm').removeAttr('enctype')
    */
}

$('#confirmButton').click(function (e) {
    e.preventDefault();

    $('#originalItemInfoContainer').append('<input type="item" id="originalItemNumberInput" name="originalItemNumber"></form>');

    document.getElementById('originalItemNumberInput').value = originalItemNumber;

    document.getElementById('itemInfoForm').submit();

    /*
    var form = $('#itemInfoForm')[0];
    var formData = new FormData(form);
    $.ajax({
        url: '/items/modify/submit',
        type: 'POST',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            window.alert(data)
        },
        error: function () {
            window.alert('Ajax error occured')
        }
    })
    */
})

$('#cancelButton').click(function (e) {
    window.location.href = '/items/listAll';
})