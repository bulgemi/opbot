/*
    file: task_new.js
    author: kim dong-hun
*/
// Validation message 초기화.
function initValidationMessage(group) {
    var g = $(group);
    g.removeClass("validation");
    g.removeClass("error");
    g.removeClass("warning");
};
// control task type
function controlTaskType() {
    var rb1 =  $('input[name="rb1"]:checked').val();

    if (rb1 === "0") {
        $('#script_group').hide();
        $('#script_theme_group').hide();
        $('#target_list_group').hide();
    } else {
        $('#script_group').show();
        $('#script_theme_group').show();
        $('#target_list_group').show();
    }
};
// '테스트 등록' button 처리
$(document).ready(function() {
    var taskUid = "";

    controlTaskType();
    // 연동 유형 변경 감지
    $('input[name="rb1"]').change(function() {
//        console.log("change!");
        controlTaskType();
    });
    // 처리 유형 변경 감지
    $('input[name="rb2"]').change(function() {
//        console.log("change!");
    });
    // 태스크 이름 유효성 검증.
    var task_name = $('#task_name');
    task_name.blur(function() {
        var rb1 =  $('input[name="rb1"]:checked').val();
        var rb2 =  $('input[name="rb2"]:checked').val();
        initValidationMessage('#task_name_group');

        if (task_name.val().length === 0) {
            $('#task_name_group').addClass("validation error");
            $('#task_name_tip').text("필수 항목입니다!");
        } else {
            taskUid = $('#task_uid').val();
//            console.log("-task_uid=[" + taskUid + "]");
            $.ajax({
                type: 'POST',
                url: $SCRIPT_ROOT + '/task/_check_task_name',
                data: {
                    task_uid: taskUid,
                    name: task_name.val(),
                    task_type: rb1,
                    action_type: rb2
                },
                dataType: 'JSON',
                success: function(data) {
//                    console.log(data.result);
                    res = data.result;

                    if (res.result === true) {
                        tip = res.detail.task_name.tip;
                        $('#task_name_tip').text(tip);
                        $('#task_uid').val(res.rdata.task_uid);
                    } else {
                        c = res.detail.task_name.class;
                        $('#task_name_group').addClass(c[0]);
                        t = res.detail.task_name.tip;
                        $('#task_name_tip').text(t[0]);
                    }
                },
                error: function(xtr, status, error) {
//                    console.log(xtr +":"+status+":"+error);
                    ;
                }
            });
        }
    });
    // 등록 사유 유효성 검증 & 처리
    var desc = $('#desc');
    desc.blur(function() {
        taskUid = $('#task_uid').val();
//        console.log("--task_uid=[" + taskUid + "]");
        initValidationMessage('#desc_group');

        if (desc.val().length === 0) {
            $('#desc_group').addClass("validation error");
            $('#desc_tip').text("필수 항목입니다!");
        } else {
            if (taskUid.length === 0) {
                $('#desc_group').addClass("validation error");
                $('#desc_tip').text("태스크 이름을 확인하세요!");
            } else {
                var rb1 = $('input[name="rb1"]:checked').val();

                $.ajax({
                    type: 'POST',
                    url: $SCRIPT_ROOT + '/task/_check_desc',
                    data: {
                        task_uid: taskUid,
                        task_type: rb1,
                        desc: desc.val()
                    },
                    dataType: 'JSON',
                    success: function(data) {
//                        console.log(data.result);
                        res = data.result;

                        if (res.result === true) {
                            tip = res.detail.desc.tip;
                            $('#desc_tip').text(tip);
                        } else {
                            c = res.detail.desc.class;
                            $('#desc_group').addClass(c[0]);
                            t = res.detail.desc.tip;
                            $('#desc_tip').text(t[0]);
                        }
                    },
                    error: function(xtr, status, error) {
//                        console.log(xtr +":"+status+":"+error);
                        ;
                    }
                });
            }
        }
    });
    // '생성' 처리
    $('#create').bind('click', function() {
        taskUid = $('#task_uid').val();
//        console.log("----task_uid=[" + taskUid + "]");
        var tl = $("#targetList").jsGrid("option", "data");
//        console.log('tl=' + tl);

        if (taskUid.length === 0) {
            $('#script_group').addClass("validation error");
            $('#script_tip').text("태스크 이름을 확인하세요!");
        } else {
            $.ajax({
                url: $SCRIPT_ROOT + '/task/_submit',
                type: 'POST',
                contentType: "application/json",
                dataType: 'JSON',
                data: JSON.stringify({
                    task_uid: taskUid,
                    target_list: tl
                }),
                success: function(data) {
//                    console.log(data.result);
                    res = data.result;

                    if (res.result === true) {
                        window.location.href = $SCRIPT_ROOT + "/task/list";
                    } else {
                        c = res.detail.script.class;
                        $('#script_group').addClass(c[0]);
                        t = res.detail.script.tip;
                        $('#script_tip').text(t[0]);
                    }
                },
                error: function(xtr, status, error) {
//                    console.log(xtr +":"+status+":"+error);
                    ;
                }
            });
        }
    });
});
