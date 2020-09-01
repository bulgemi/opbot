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
    del_id = "#" + id;
    del_tree = "#t_" + id;
    $(del_id).remove();
    $(del_tree).remove();
    return false;
};
// get click event(task)
function del_task(id) {
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
    // get click event(group member)
    $('#add_member').click(function(e) {
        initValidationMessage('#group_member_name');
        var member_info = $('#group_member');

        if (member_info.val().length == 0) {
            $('#group_member_name').addClass("validation error");
            $('#group_member_tip').text("그룹 멤버 이름이 없습니다!");
        } else {
            $.ajax({
                type: 'POST',
                url: $SCRIPT_ROOT + '/group/_check_group_member',
                data: {
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
});