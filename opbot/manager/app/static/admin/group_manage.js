/*
    file: group_manage.js
    author: kim dong-hun
*/
$(document).ready(function() {
    // Search 버튼.
    $('#search').bind('click', function() {
        var cond1 = $("#cond1 option:selected").val();
        var some =  $("#some").val();

        $.ajax({
            url: $SCRIPT_ROOT + '/admin/_search_group_list',
            type: 'POST',
            contentType: "application/json",
            dataType: 'JSON',
            data: JSON.stringify({
                cond1: cond1,
                some: some
            }),
            success: function(response) {
                console.log(response.result);
                // location.reload(true);
                $("#groupList").jsGrid("option", "data", response.result);
            },
            error: function(xtr, status, error) {
                console.log(xtr +":"+status+":"+error);
            }
        });
    });
});