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