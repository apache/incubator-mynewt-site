
/* Highlight */
$( document ).ready(function() {
    hljs.initHighlightingOnLoad();
    $('table').addClass('table table-striped table-hover');
});

/* Prevent disabled links from causing a page reload */
$("li.disabled a").click(function() {
    event.preventDefault();
});

function fixDocSidebar() {
    var sidebarHeight = $("#docSidebar").height();
    console.log('sidebar at ' + sidebarHeight);

    var visibleHeight = $( window ).height() - $('#navbar').height();
    console.log('visible at ' + visibleHeight);

    // Fix the sidebar height to the visible window
    $("#docSidebar").css("height", visibleHeight);

    // If the sidebar content is larger than visible height give it scrollability.
    if (sidebarHeight <= visibleHeight) {
        $("#docSidebar").css("overflow-y", "hidden");
    }
    else {
        $("#docSidebar").css("overflow-y", "scroll");
    }
}

$( document ).ready(function() {
    $("#docSidebar").css("overflow-x", "hidden");
    fixDocSidebar();
    $( window ).on('resize', fixDocSidebar);
});
