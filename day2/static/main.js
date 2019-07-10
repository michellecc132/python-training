$( document ).ready(function() {
    $("a").click(function( event ) {
        alert("Thanks for visiting!!");
    });

    $("#hider").click(function( event ) {
        //$(".experiment").toggle();
        if ($(".experiment").hasClass("testing")) {
            $(".experiment").removeClass("testing");
        } else {
            $(".experiment").addClass("testing");
        }
    });

    $("#zip").click(function(event) {
        $.get('/zip', function(data) {
            $("#my-zip").html(data);
        })
    });
});
