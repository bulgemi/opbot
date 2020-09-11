/*
    file: group_manage_db.js
    author: kim dong-hun
*/
(function() {
    var db = {
        loadData: function(filter) {
            console.log("filter=", filter);

            groupUid = $('#group_uid').val();
            var d = $.Deferred();

            $.ajax({
                url: $SCRIPT_ROOT + '/admin/_load_group_list',
                type: 'POST',
                contentType: "application/json",
                dataType: "JSON",
                data: JSON.stringify({
                    group_uid: groupUid,
                    filter: filter
                }),
            }).done(function(response) {
                d.resolve(response.result);
            });

            return d.promise();
        },
        insertItem: function(insertingGroup) {
            console.log("insertingGroup=", insertingGroup);
        },
        updateItem: function(updatingGroup) {
            console.log("updatingGroup=", updatingGroup)
        },
        deleteItem: function(deletingGroup) {
            console.log("deletingGroup=", deletingGroup)
            $.ajax({
                url: $SCRIPT_ROOT + '/admin/_delete_group',
                type: 'POST',
                contentType: "application/json",
                dataType: "JSON",
                data: JSON.stringify(deletingGroup),
            }).done(function(response) {
                console.log("response=", response);
            });
        }
    };

    window.db = db;
}());