/*
    file: task_list.js
    author: kim dong-hun
*/
$(document).ready(function() {
    // 검색조건 1
    $("#cond1").change(function() {
        var cond1 = $("#cond1 option:selected").val();
        console.log("change cond1:" + cond1);
    });
    // 검색조건 2
    $("#cond2").change(function() {
        var cond2 = $("#cond2 option:selected").val();
        console.log("change cond2:" + cond2);
    });
    // Search 버튼.
    $('#search').bind('click', function() {
        var cond1 = $("#cond1 option:selected").val();
        var cond2 = $("#cond2 option:selected").val();
        var some =  $("#some").val();

        console.log("click search.");
        $.ajax({
            url: $SCRIPT_ROOT + '/task/_search_task_list',
            type: 'POST',
            contentType: "application/json",
            dataType: 'JSON',
            data: JSON.stringify({
                cond1: cond1,
                cond2: cond2,
                some: some
            }),
            success: function(response) {
                console.log(response.result);
                // location.reload(true);
                $("#taskList").jsGrid("option", "data", response.result);
            },
            error: function(xtr, status, error) {
                console.log(xtr +":"+status+":"+error);
            }
        });
    });
});
