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
// get click event(members)
function del_member(id) {
    event.preventDefault();
    del_id = "#" + id;
    del_tree = "#t_" + id;
    $(del_id).remove();
    $(del_tree).remove();
    $("#task_list").children("div").remove();
    return false;
};
// get click event(task)
function del_task(id) {
    event.preventDefault();
    del_id = "#" + id;
    $(del_id).remove();
    return false;
};
// get click event(task)
function add_task(t, n) {
    console.log(t, n);
    var el_fmt = "<div class='align-center right-padding top-padding' id='div"+ t +"'>"+ "<button class='ink-button' id='"+ t +"' title='"+ n +"' onclick=\"del_task('div"+ t +"')\">"+ n + "</button></div>";
    $("#task_list").append(el_fmt);
    return false;
};
// '그룹 등록' button 처리
$(document).ready(function() {
    $('#formid').on('keyup keypress', function(e) {
        var keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            e.preventDefault();
            return false;
        }
    });
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
     // 그룹 멤버 정보 조회
    var member_info = $('#group_member');
    member_info.blur(function() {
        initValidationMessage('#group_member_name');

        if (member_info.val().length == 0) {
            $('#group_member_name').addClass("validation error");
            $('#group_member_tip').text("그룹 멤버 이름이 없습니다!");
        } else {
            $.ajax({
                type: 'POST',
                url: $SCRIPT_ROOT + '/group/_check_group_member',
                data: {
                    group_name: $('#group_name').val(),
                    member_info: member_info.val()
                },
                dataType: 'JSON',
                success: function(data) {
                    res = data.result;
                    console.log(res);

                    if (res.result == true) {
                        tip = res.detail.member_infos.tip;
                        $('#group_member_tip').text(tip);
                        members = res.detail.members;

                        for (i=0; i < members.length; i++) {
                            var el_val = members[i];
                            var gm_el_fmt = "<div class='align-center right-padding top-padding' id='member_"+ i +"'>"+ "<button class='ink-button' id='"+ el_val['email'] +"' title='"+ el_val['email'] +"' onclick=\"del_member('member_"+ i +"')\">"+ el_val['name'] + "</button></div>";
                            console.log(gm_el_fmt);
                            $("#member_list").append(gm_el_fmt);

                            var tasks = el_val['task_info'];
                            console.log("tasks.length=" + tasks.length)
                            tr_el_fmt = "<li class=\"parent open\" data-open=\"true\" id=\"t_member_"+ i +"\"><i class=\"fa fa-minus-circle\"></i><a href=\"#\">"+ el_val['name'] +"</a>";
                            tr_el_fmt += "<ul class>";
                            for (var l=0; l < tasks.length; l++) {
                            var task = tasks[l];
                              tr_el_fmt += "<li><a href=\"#\" onclick=\"add_task('"+ task['task_id'] +"', '"+ task['task_name'] +"')\">"+ task['task_name'] +"</a></li>";
                            }
                            tr_el_fmt += "</ul>";
                            tr_el_fmt += "</li>";
                            console.log("tr_el_fmt=" + tr_el_fmt)
                            $("#tasks_info").append(tr_el_fmt);
                        }
                    } else {
                        c = res.detail.member_infos.class;
                        $('#group_member_name').addClass(c[0]);
                        t = res.detail.member_infos.tip;
                        $('#group_member_tip').text(t[0]);
                    }
                },
                error: function(xtr, status, error) {
                    console.log(xtr +":"+status+":"+error);
                }
            });
        }
    });
    // '생성' 처리
    $('#save_group').bind('click', function() {
        var group_name = $("#group_name").val();
        var member_list = $("#member_list").find("button");
        var task_list = $("#task_list").find("button");
        var member_array = [];
        var task_array = [];

        for (var i=0; i < member_list.length; i++) {
            var member_el = member_list[i]
            member_array.push(member_el["id"])
        }

        for (var i=0; i < task_list.length; i++) {
            var task_el = task_list[i]
            task_array.push(task_el["id"])
        }
        console.log("------------>", group_name);
        console.log("------------>", member_array);
        console.log("------------>", task_array);

        if (group_name.length == 0) {
            $('#group_name_group').addClass("validation error");
            $('#group_name_tip').text("필수 항목입니다!");
        } else {
            $.ajax({
                url: $SCRIPT_ROOT + '/group/_submit',
                type: 'POST',
                contentType: "application/json",
                dataType: 'JSON',
                data: JSON.stringify({
                    group_name: group_name,
                    member_list: member_array,
                    task_list: task_array
                }),
                success: function(data) {
                    console.log(data.result);
                    res = data.result;

                    if (res.result === true) {
                        window.location.href = $SCRIPT_ROOT + "/group/list";
                    } else {
                        c = res.detail.script.class;
                        $('#group_name_group').addClass(c[0]);
                        t = res.detail.script.tip;
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