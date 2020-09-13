/*
    file: user_manage_db.js
    author: kim dong-hun
*/
(function() {
    var db = {
        loadData: function(filter) {
            console.log("filter=", filter);

            userUid = $('#user_uid').val();
            var d = $.Deferred();

            $.ajax({
                url: $SCRIPT_ROOT + '/admin/_load_user_list',
                type: 'POST',
                contentType: "application/json",
                dataType: "JSON",
                data: JSON.stringify({
                    user_uid: userUid,
                    filter: filter
                }),
            }).done(function(response) {
                d.resolve(response.result);
            });

            return d.promise();
        },
        insertItem: function(insertingUser) {
            console.log("insertingUser=", insertingUser);

            $.ajax({
                url: $SCRIPT_ROOT + '/admin/_add_user',
                type: 'POST',
                contentType: "application/json",
                dataType: "JSON",
                data: JSON.stringify(insertingUser),
            }).done(function(response) {
                console.log("response=", response);
                location.reload();
            });
        },
        updateItem: function(updatingUser) {
            console.log("updatingUser=", updatingUser)
             $.ajax({
                url: $SCRIPT_ROOT + '/admin/_update_user',
                type: 'POST',
                contentType: "application/json",
                dataType: "JSON",
                data: JSON.stringify(updatingUser),
            }).done(function(response) {
                console.log("response=", response);
                location.reload();
            });
        },
        deleteItem: function(deletingUser) {
            console.log("deletingUser=", deletingUser)
            $.ajax({
                url: $SCRIPT_ROOT + '/admin/_delete_user',
                type: 'POST',
                contentType: "application/json",
                dataType: "JSON",
                data: JSON.stringify(deletingUser),
            }).done(function(response) {
                console.log("response=", response);
                location.reload();
            });
        }
    };

    window.db = db;

    db.role = [
        {Name: "일반 사용자", Id: 2},
        {Name: "그룹 관리자", Id: 1},
        {Name: "관리자", Id: 0}
    ];
    db.status = [
        {Name: "잠금", Id: 0},
        {Name: "활성", Id: 1},
    ];
}());