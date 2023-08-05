var articleEdit = Boolean($("meta[name=\"article-edit\"]").attr("content"));
var clipboard = new Clipboard('.btn-article-file-url');
function articleCreate(selector) {
    $("#article-edit-submit-message").html('Submitting...');
    var submit = $.ajax({
        type: "POST",
        url: $(selector).attr("data-submit-url"),
        data: {
            "html": true,
            "markdown": true,
        },
    });
    submit.done(function (r) {
        if (r.submitted) {
            $("#article-submit-message").html('<span class="submitted">Submitted.</span>');
            var redirect = $(selector).attr("data-redirect-url").replace("0", r.data.id);
            if ($("meta[name='no-redirect']").attr("content") != "True") {
                window.location.replace(redirect);
            }
        }
        else {
            $("#article-submit-message").html('<span class="error">An error occured when submitting. See the console for details.</span>');
            console.log('Article creation error:\n', r);
        }
    });
    submit.fail(function (response) {
        $("#article-submit-message").html('<span class="error">An error occured when submitting: ' + response.status + '</span>');
    });
}
function articleEditSubmit() {
    $("#article-edit-submit-message").html('Submitting...');
    var submit = $.ajax({
        type: "POST",
        url: $("#article-edit-submit").attr("action"),
        data: $("#article-edit-submit").serialize()
    });
    submit.done(function (r) {
        if (r.submitted) {
            $("#article-edit-submit-message").html('<span class="submitted" >Submitted.</span>');
            setTimeout(function () {
                $("#article-edit-submit-message .submitted").fadeOut();
            }, 3000);
        }
        else {
            if (r.error.code == "form_invalid") {
                $("#article-edit-submit-message").html("<span>Submitted.</span>");
                $("#article-edit-submit-message .inputs").html(r.form);
            }
            else {
                $("#article-edit-submit-message").html('<span class="error">An error occured when submitting. See the console for details.</span>');
                console.log('Article ' + articleEdit ? 'edit' : 'creation' + ' error:\n', r);
            }
        }
    });
    submit.fail(function (response) {
        $("#article-edit-submit-message").html('<span class="error">An error occured when submitting: ' + response.status + '</span>');
    });
}
function renderFileThumbnail(data) {
    var image;
    if (data.file.image) {
        image = "<img class=\"media-object\" src=\"" + data.file.url + "\" alt=\"Image Thumbnail\" />";
    }
    else {
        image = "<img class=\"media-object\" src=\"/static/img/article-file-placeholder.png\" alt=\"Image Thumbnail Placeholder\" />";
    }
    var fileThumbnail = "\n        <div class=\"media article-file-item\" id=\"article-file-item-" + data.id + "\">\n            <div class=\"input-group article-file-url\">\n                <input type=\"text\" class=\"form-control\" value=\"" + data.file.name + "\" readonly />\n                <span class=\"input-group-btn\">\n                    <button class=\"btn btn-default btn-article-file-url\" type=\"button\" data-clipboard-text=\"" + data.file.url + "\" title=\"Copy URL\">\n                        <i class=\"fa fa-clipboard\" aria-hidden=\"true\"></i>\n                    </button>\n                </span>\n            </div>\n            <div class=\"media-left\">" + image + "</div>\n            <div class=\"media-body\">\n                <div id=\"article-file-options-" + data.id + "\">\n                    <button class=\"btn btn-danger btn-article-file-delete\" onclick=\"articleFileDelete('" + data.id + "', '" + data.file.url + "')\">\n                        <i class=\"fa fa-trash-o\" aria-hidden=\"true\"></i>\n                    </button>\n                    <a class=\"btn btn-primary btn-article-file-edit\" href=\"/admin/article/articlefile/" + data.id + "/change/\" target=\"_blank\">\n                        <i class=\"fa fa-pencil-square-o\" aria-hidden=\"true\"></i>\n                    </a>\n                </div>\n            </div>\n        </div>\n    ";
    $("#article-file-list").prepend(fileThumbnail);
    $("#article-file-empty").remove();
}
Dropzone.options.articleFileSubmit = {
    paramName: "associated_file",
    maxFilesize: 1000,
    parallelUploads: 10,
    headers: {
        "X-CSRFToken": Cookies.get("csrftoken"),
    },
    init: function () {
        this.on("success", function (file, r) {
            this.removeFile(file);
            if (r.submitted) {
                $("#article-file-upload-message").html("");
                renderFileThumbnail(r.data);
            }
            else {
                $("#article-file-upload-message").html('<span class="error">An error occured when submitting. See the console for details.</span>');
                console.log('Article file upload error:\n', r);
            }
        });
    },
};
function articleFileDelete(id, path) {
    var deleteConfirm = "\n        <div id=\"article-file-delete-" + id + "\" class=\"article-file-delete\">\n            <button class=\"btn btn-danger\" onclick=\"articleFileDeleteConfirm('" + id + "', '" + path + "')\">Yes</button>\n            <button class=\"btn btn-success\" onclick=\"articleFileDeleteCancel('" + id + "')\">No</button>\n        </div>\n    ";
    $("#article-file-options-" + id).append(deleteConfirm);
    $("#article-file-options-" + id + " .btn-article-file-delete").prop("disabled", true);
}
function articleFileDeleteConfirm(id, path) {
    $("#article-file-delete-" + id).html("<span>Deleting...</span>");
    var submit = $.ajax({
        type: "POST",
        url: "/api/articles/file/delete/",
        data: { id: id, path: path }
    });
    submit.done(function (r) {
        if (r.submitted) {
            $('#article-file-item-' + id).remove();
        }
        else {
            $("#article-file-delete-" + id).html('<span class="error">An error occured when deleting. See the console for details.</span>');
            console.log('Article file deletion error:\n', r);
            $("#article-file-options-" + id + " .btn-article-file-delete").prop("disabled", false);
        }
    });
    submit.fail(function (response) {
        $("#article-file-delete-" + id).html('<span class="error">An error occured when deleting: ' + response.status + '</span>');
        $("#article-file-options-" + id + " .btn-article-file-delete").prop("disabled", false);
    });
}
function articleFileDeleteCancel(id) {
    $("#article-file-delete-" + id).remove();
    $("#article-file-options-" + id + " .btn-article-file-delete").prop("disabled", false);
}
