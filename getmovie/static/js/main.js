$(function() {

	$('#open-menu').on('click', function(){
		$('.wrapper').addClass('opened-menu');
		$('.main-menu').addClass('opened-menu');
	});
	$('#close-menu').on('click', function(){
		$('.wrapper').removeClass('opened-menu');
		$('.main-menu').removeClass('opened-menu');
	});

	$('#get-film').on("submit", function(){
		event.preventDefault();
		$.ajax({
		    type: "POST",
		    url: '/',
		    data: {
		      'csrfmiddlewaretoken': $( "input[name='csrfmiddlewaretoken']" ).val(),
			  'random': true,
			  'type': 'movie',
		    },
		    dataType: 'json',
		    success: function (data) {
		      console.log(data);
		    }
	  });
	});
});
