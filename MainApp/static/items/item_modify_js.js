var originalCategory;
var originalItemNumber;
var originalName;
var itemNumberBackup;

function categoryCheck(that) {
    if (that.value != 'Learning') {
        $('#itemNumberInput').attr('disabled', true);
        $('#itemNumberOuterContainer').attr('style', 'display: none;');
        document.getElementById('nameInput').placeholder = '請輸入項目名稱';
    }
    else {
        $('#learningOptionNoInput').prop('checked', true);
        learningOptionCheck(document.getElementById('learningOptionNoInput'));
        $('#itemNumberOuterContainer').removeAttr('style');
        document.getElementById('nameInput').placeholder = '請輸入課程名稱';
    }
}

function learningOptionCheck(that) {
    if (that.value == 'yes') {
        $('#itemNumberInput').removeAttr('disabled');
        document.getElementById('itemNumberInput').value = '';
        $('#itemNumberContainer').removeAttr('style');
    }
    else {
        $('#itemNumberInput').attr('disabled', true);
        $('#itemNumberContainer').attr('style', 'display: none;');
    }
}

function recordAndSetInfo() {
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
    originalCategory = document.getElementById('originalCategoryInput').value;
    originalItemNumber = document.getElementById("itemNumberInput").value;
    originalName = document.getElementById('nameInput').value;
    
    $('#categorySelect').val(document.getElementById('originalCategoryInput').value).change();

    if (document.getElementById('categorySelect').value != 'Learning') {
        itemNumberBackup = document.getElementById("itemNumberInput").value;
    }

    $('#originalCategoryInput').remove();

    /*
    $('#itemInfoForm').attr('action', '/items/modify/submit')
    $('#itemInfoForm').attr('method', 'post')
    $('#itemInfoForm').removeAttr('enctype')
    */
}

$('#itemInfoForm').on('submit', function (e) {
    e.preventDefault();

    $('#itemNumberInput').removeAttr('disabled');

    if (document.getElementById('categorySelect').value != 'Learning') {
        document.getElementById("itemNumberInput").value = itemNumberBackup;
    }

    $('#originalItemInfoContainer').append('<input type="text" id="originalCategoryInput" name="originalCategory">');
    $('#originalItemInfoContainer').append('<input type="text" id="originalItemNumberInput" name="originalItemNumber">');
    $('#originalItemInfoContainer').append('<input type="text" id="originalNameInput" name="originalName">');

    document.getElementById('originalCategoryInput').value = originalCategory;
    document.getElementById('originalItemNumberInput').value = originalItemNumber;
    document.getElementById('originalNameInput').value = originalName;

    var form = $('#itemInfoForm')[0];
    var formData = new FormData(form);

    $.ajax({
        url: '/items/modify/check',
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
                $('#originalCategoryInput').remove();
                $('#originalItemNumberInput').remove();
                $('#originalNameInput').remove();
            }
        },
        error: function () {
            window.alert('Ajax error occured');
        }
    })
})

$('#cancelButton').click(function (e) {
    window.location.href = '/items/listAll';
})