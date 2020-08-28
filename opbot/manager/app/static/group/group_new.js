/*
    file: group_new.js
    author: kim dong-hun
*/
// Validation message 초기화.
function initValidationMessage(group) {
    var g = $(group);
    g.removeClass("validation");
    g.removeClass("error");
    g.removeClass("warning");
};
// '그룹 등록' button 처리
$(document).ready(function() {
    // 그룹 이름 유효성 검증.
    var group_name = $('#group_name');
    group_name.blur(function() {
        initValidationMessage('#group_name_group');

        if (group_name.val().length == 0) {
            $('#group_name_group').addClass("validation error");
            $('#group_name_tip').text("필수 항목입니다!");
        } else {
            $.ajax({
                type: 'POST',
                url: $SCRIPT_ROOT + '/group/_check_group_name',
                data: {
                    group_name: group_name.val()
                },
                dataType: 'JSON',
                success: function(data) {
                    res = data.result;
                    console.log(res);

                    if (res.result == true) {
                        tip = res.detail.group_name.tip;
                        $('#group_name_tip').text(tip);
                    } else {
                        c = res.detail.group_name.class;
                        $('#group_name_group').addClass(c[0]);
                        t = res.detail.group_name.tip;
                        $('#group_name_tip').text(t[0]);
                    }
                },
                error: function(xtr, status, error) {
                    console.log(xtr +":"+status+":"+error);
                }
            });
        }
    });
});
