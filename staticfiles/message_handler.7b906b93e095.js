$(document).ready(function () {
    "use strict";

    /* timer for refresh function
     * refresh comments after 5 seconds */
    function push() {
        window.setTimeout(function () {
            refresh_discussion_comments();
            push();
        }, 5000);
    }

    /* loads discussion_comments */
    function refresh_discussion_comments() {
        /* extract discussion_id from url
         * id is assumed to be the 3rd element from zero */
        let path = window.location.pathname;
        let discussion_id = path.split("/")[2];
        /* call url of view and gets rendered html for template */
        $.ajax({
            url: "/discussion/" + discussion_id + "/get_discussion_comments/", success: function (result) {
                $("#discussion_comments").empty();
                $("#discussion_comments").append(result);
            }
        });
    }

    /* load discussion_comments if page == discussion page */
    if (window.location.pathname.split("/")[1].localeCompare("discussion") === 0) {
        /* load discussion_comments on page load */
        refresh_discussion_comments();
        /* start timer*/
        push();
    }

});
