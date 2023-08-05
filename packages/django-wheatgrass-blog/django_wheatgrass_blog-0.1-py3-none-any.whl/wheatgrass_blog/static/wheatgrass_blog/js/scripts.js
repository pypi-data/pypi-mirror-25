function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(parseString(settings.type && !this.crossDomain))) {
            xhr.setRequestHeader("X-CSRFToken", parseString(Cookies.get("csrftoken")));
        }
    }
});
function $_GET(variable, notFound) {
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=");
        if (pair[0] == variable) {
            return pair[1];
        }
    }
    return notFound;
}
function parseString(object) {
    switch (typeof (object)) {
        case "string":
            return object;
        case "number":
        case "boolean":
            return object.toString();
        case "undefined":
            try {
                return object.toString();
            }
            catch (TypeError) {
                return "";
            }
        default:
            return "";
    }
}
function clearFormInputs(selector) {
    var textInputTypes = [
        "text",
        "number",
        "url",
        "email",
        "password",
        "tel",
    ];
    textInputTypes.forEach(function (type) {
        $(selector + " input[type=\"" + type + "\"]").val("");
    });
    $(selector + " textarea").val("");
}
