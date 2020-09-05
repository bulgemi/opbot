/*
    file: task_list_db.js
    author: kim dong-hun
*/
(function() {
    var db = {
        loadData: function(filter) {
            console.log("filter=", filter);

            taskUid = $('#task_uid').val();
            var d = $.Deferred();

            $.ajax({
                url: $SCRIPT_ROOT + '/task/_load_task_list',
                type: 'POST',
                contentType: "application/json",
                dataType: "JSON",
                data: JSON.stringify({
                    task_uid: taskUid,
                    filter: filter
                }),
            }).done(function(response) {
                d.resolve(response.result);
            });

            return d.promise();
        },
        insertItem: function(insertingTask) {
            console.log("insertingTask=", insertingTask);
        },
        updateItem: function(updatingTask) {
            console.log("updatingTask=", updatingTask)
        },
        deleteItem: function(deletingTask) {
            console.log("deletingTask=", deletingTask)
            $.ajax({
                url: $SCRIPT_ROOT + '/task/_delete_task',
                type: 'POST',
                contentType: "application/json",
                dataType: "JSON",
                data: JSON.stringify(deletingTask),
            }).done(function(response) {
                console.log("response=", response);
            });
        }
    };

    window.db = db;
}());