$(document).ready(function(){
  var heightScreen=window.innerHeight;

  $("#hiddenPart").css('height', heightScreen);
  $("#hamburger").click(function(){
  	if ($(this).hasClass("opened"))
  	{
	    $(this).removeClass('opened');
	    $(this).addClass('closed');
	  	$(this).animate({
	        "left": "0%"
	    }, "slow");

	  	$("#hiddenPart").animate({
	        "left": "-80%"
	    }, "slow");
	}else{
		$(this).removeClass('closed');
		$(this).addClass('opened');
		$(this).animate(
		{
		   "left": "80%"
		}, "slow");

	  	$("#hiddenPart").animate({
	        "left": "0%"
	    }, "slow");
	}
	
  });

})