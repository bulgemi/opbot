(function() {
    var db = {
        loadData: function(filter) {
            taskUid = $('#task_uid').val();
            var d = $.Deferred();

            console.log("filter=", filter);
            console.log("task_uid=", taskUid);

            $.ajax({
                url: $SCRIPT_ROOT + '/task/_load_target_list',
                type: 'POST',
                contentType: "application/json",
                dataType: "JSON",
                data: JSON.stringify({
                    task_uid: taskUid,
                    filter: filter
                }),
                success: function(response) {
                    d.resolve(response.result);
                },
                error: function(xtr, status, error) {
                    console.log(xtr +":"+status+":"+error);
                }
            });

            return d.promise();
        },
        insertItem: function(insertingTarget) {
            console.log("insertingTarget=", insertingTarget);
            var tl = $("#targetList").jsGrid("option", "data");
        },
        updateItem: function(updatingTarget) {
            console.log("updatingTarget=", updatingTarget)
            var tl = $("#targetList").jsGrid("option", "data");
        },
        deleteItem: function(deletingTarget) {
            console.log("deletingTarget=", deletingTarget)
            var tl = $("#targetList").jsGrid("option", "data");
        }
    };

    window.db = db;
}());