$(function() {
	let film = {
		img: $('.generated-film__info--img img'),
		title: $('.generated-film__info--detail .title'),
		genre: $('.generated-film__info--detail .genre'),


		show: function(data){
			film.img.attr('src', 'https://image.tmdb.org/t/p/w500/' + data.poster_path);
			film.title.html(data.title);

			setTimeout(function(){
				$('.h__update').addClass('h__update--show');
				$('body').addClass('--generated-film');
				$('#get-film').hide();
				$('#generated-film').show();
				$('#generated-film, #header').animate({opacity: '1'}, 500);
				$('#generated-film, #header').removeClass('scale07');
			}, 500);
		},
		hide: function(){
			menu.close();
			$('#generated-film, #header').animate({opacity: '0'}, 500);
			$('#generated-film, #header').addClass('scale07');
		},

		generate: function(){
			$.ajax({
			    type: "POST",
			    url: '/',
				beforeSend: function(){
					film.hide();
					preloader.start();
			    },
			    data: {
			      'csrfmiddlewaretoken': $( "#get-film input[name='csrfmiddlewaretoken']" ).val(),
				  'random': true,
				  'type': 'movie',
			    },
			    dataType: 'json',
			    success: function (data) {
				  setTimeout(function(){
					  film.show(data);
				  }, 600);
			      console.log(data);
			    }
		  });
		},

	}

	let menu = {
		open: function(){
			$('body').addClass('opened-menu');
		},
		close: function(){
			$('body').removeClass('opened-menu');
		},
	}

	let preloader = {
		start: function(){
			menu.close();
			$('#get-film, #header').animate({opacity: '0'}, 5);
			$('#get-film, #header').addClass('scale07');
		},
		stop: function(){
			menu.close();
			$('#get-film, #header').animate({opacity: '1'}, 5);
			$('#get-film, #header').removeClass('scale07');
		}
	}
	// Работа кнопок
	$('#open-menu').on('click', function(){
		menu.open();
	});
	$('#close-menu').on('click', function(){
		menu.close();
	});
	$('#header-get-film').on('click', function(){
		film.generate();
	});
	// Работа кнопок END

	// AJAX ЗАПРОС на рандомный фильм без фильтров
	$('#get-film').on("submit", function(){
		event.preventDefault();
		film.generate();
	});


});
