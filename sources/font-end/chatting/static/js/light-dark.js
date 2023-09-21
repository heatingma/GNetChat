!function(a) {
    "use strict";
    a("#light-dark").on("click", function(t) {
        console.log("click!");
        if ("disabled" !== a("#bootstrap-style").attr("disabled")) {
            a("#bootstrap-dark-style").attr("disabled", !1);
            a("#bootstrap-style").attr("disabled", !0);
            a("#side-menu-dark-style").attr("disabled", !1);
            a("#side-menu-style").attr("disabled", !0);
        } else {
            a("#bootstrap-dark-style").attr("disabled", !0);
            a("#bootstrap-style").attr("disabled", !1);
            a("#side-menu-dark-style").attr("disabled", !0);
            a("#side-menu-style").attr("disabled", !1);
        }
    });
  
}(jQuery);