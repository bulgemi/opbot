// user_new.js
// Validation message 초기화.
function initValidationMessage(group) {
    var g = $(group);
    g.removeClass("validation");
    g.removeClass("error");
    g.removeClass("warning");
};

$(document).ready(function(){
    // validate name
    var name = $('#name');
    name.blur(function() {
        initValidationMessage('#name_group');

        if (name.val().length == 0) {
            $('#name_group').addClass("validation error");
            $('#name_tip').text("필수 항목입니다!");
        } else {
            $.ajax({
                type: 'POST',
                url: $SCRIPT_ROOT + '/_check_username',
                data: {
                    name: $('#name').val()
                },
                dataType: 'JSON',
                success: function(data) {
//                    console.log(data.result);
                    res = data.result;

                    if (res.result === true) {
                        tip = res.detail.name.tip;
                        $('#name_tip').text(tip);
                    } else {
                        c = res.detail.name.class;
                        $('#name_group').addClass(c[0]);
                        t = res.detail.name.tip;
                        $('#name_tip').text(t[0]);
                    }
                },
                error: function(xtr, status, error) {
                    console.log(xtr +":"+status+":"+error);
                }
            });
        }
    });
    // validate email
    var email = $('#email');
    email.blur(function() {
        initValidationMessage('#email_group');

        if (email.val().length == 0) {
            $('#email_group').addClass("validation error");
            $('#email_tip').text("필수 항목입니다!");
        } else {
            $.ajax({
                type: 'POST',
                url: $SCRIPT_ROOT + '/_check_email',
                data: {
                    email: $('#email').val()
                },
                dataType: 'JSON',
                success: function(data) {
//                    console.log(data.result);
                    res = data.result;

                    if (res.result === true) {
                        tip = res.detail.email.tip;
                        $('#email_tip').text(tip);
                    } else {
                        c = res.detail.email.class;
                        $('#email_group').addClass(c[0]);
                        t = res.detail.email.tip;
                        $('#email_tip').text(t[0]);
                    }
                },
                error: function(xtr, status, error) {
                    console.log(xtr +":"+status+":"+error);
                }
            });
        }
    });
    // validate password
    var password = $('#password');
    password.blur(function() {
        initValidationMessage('#password_group');

        if (password.val().length == 0) {
            $('#password_group').addClass("validation error");
            $('#password_tip').text("필수 항목입니다!");
        } else {
            $.ajax({
                type: 'POST',
                url: $SCRIPT_ROOT + '/_check_password',
                data: {
                    password: $('#password').val()
                },
                dataType: 'JSON',
                success: function(data) {
//                    console.log(data.result);
                    res = data.result;

                    if (res.result === true) {
                        tip = res.detail.password.tip;
                        $('#password_tip').text(tip);
                    } else {
                        c = res.detail.password.class;
                        $('#password_group').addClass(c[0]);
                        t = res.detail.password.tip;
                        $('#password_tip').text(t[0]);
                    }
                },
                error: function(xtr, status, error) {
                    console.log(xtr +":"+status+":"+error);
                }
            });
        }
    });
    // validate password2
    var password2 = $('#password2');
    password2.blur(function() {
        initValidationMessage('#password2_group');

        if (password2.val().length == 0) {
            $('#password2_group').addClass("validation error");
            $('#password2_tip').text("필수 항목입니다!");
        } else if (password.val() === password2.val()) {
            $('#password2_tip').text("OK");
        } else {
            $('#password2_group').addClass("validation error");
            $('#password2_tip').text("패스워드가 불일치합니다!");
        }
    });
});
