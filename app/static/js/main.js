var data = jQuery('#filter').data('filter');
console.log(data);

function toggleFilterMenu() {
    $('body').css('background-color', '#FF0000');
    $('body').prepend( $("<div class='alert alert-danger' style='color:white; font-weight:bold;'>Not yet implemented</div>") )
    console.error("Not implemented yet!");
}