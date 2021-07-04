function categoryCheck(that) {
    if (that.value != 'Learning') {
        $('#itemNumberInput').attr('disabled', true);
        $('#itemNumberOuterContainer').attr('style', 'display: none;');
        document.getElementById('nameInput').placeholder = '請輸入項目名稱';
    }
    else {
        document.getElementById('learningOptionNoInput').checked = true;
        $('#itemNumberInput').attr('disabled', true);
        $('#itemNumberContainer').attr('style', 'display: none;');
        $('#itemNumberOuterContainer').removeAttr('style');
        document.getElementById('nameInput').placeholder = '請輸入課程名稱';
    }
}

function learningOptionCheck(that) {
    if (that.value == 'yes') {
        $('#itemNumberInput').removeAttr('disabled');
        $('#itemNumberContainer').removeAttr('style');
    }
    else {
        $('#itemNumberInput').attr('disabled', true);
        $('#itemNumberContainer').attr('style', 'display: none;');
    }
}


$('#itemInfoForm').on('submit', function (e) {
    e.preventDefault();

    $('#itemNumberInput').removeAttr('disabled');

    var form = $('#itemInfoForm')[0];
    var formData = new FormData(form);
    
    $.ajax({
        url: '/items/input/check',
        type: 'POST',
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: function (data) {
            if (data == 'Y') {
                document.getElementById('itemInfoForm').submit();
            }
            else {
                window.alert(data);
            }
        },
        error: function () {
            window.alert('Ajax error occured');
        }
    })
})
