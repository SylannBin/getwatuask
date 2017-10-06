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

  $(".editButton").click(function(){
  	alert("This project has been updated. An email has been sent to your professional address.")
  });

  $(".createButton").click(function(){
  	alert("The project has been created. An email has been sent to your professional address.")
  });

  $("#cancel").click(function(){
  	alert("This project has been deleted.")
  });

})