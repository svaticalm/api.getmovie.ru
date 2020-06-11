$(function() {
	// Работа кнопок
	$('#open-menu').on('click', function(){
		openMenu()
	});
	$('#close-menu').on('click', function(){
		closeMenu()
	});
	// Работа кнопок END

	// AJAX ЗАПРОС на рандомный фильм без фильтров
	$('#get-film').on("submit", function(){
		event.preventDefault();
		getFilm();
	});
	$('#header-get-film').on('click', function(){
		getFilm();
	});
	function getFilm(){
		$.ajax({
		    type: "POST",
		    url: '/',
			beforeSend: function(){
				hideFilm();
				startPreloader();
		    },
		    data: {
		      'csrfmiddlewaretoken': $( "#get-film input[name='csrfmiddlewaretoken']" ).val(),
			  'random': true,
			  'type': 'movie',
		    },
		    dataType: 'json',
		    success: function (data) {
			  showFilm(data);
		      console.log(data);
		    }
	  });
	}
	function openMenu(){
		$('.wrapper').addClass('opened-menu');
		$('.main-menu').addClass('opened-menu');
	}
	function closeMenu(){
		$('.wrapper').removeClass('opened-menu');
		$('.main-menu').removeClass('opened-menu');
	}
	function startPreloader(){
		closeMenu();
		$('#get-film, #header').animate({opacity: '0'}, 5);
		$('#get-film, #header').addClass('scale07');

	}

	let film = {
		img: $('.generated-film__info--img img'),
		title: $('.generated-film__info--detail .title'),
		genre: $('.generated-film__info--detail .genre'),
	}

	function showFilm(data){
		film.img.attr('src', 'https://image.tmdb.org/t/p/w500/' + data.poster_path);
		film.title.html(data.title);
		setTimeout(function(){
			$('.h__update').addClass('h__update--show');
			$('.content').addClass('content-generated-film');
			$('#get-film').hide();
			$('#generated-film').show();
			$('#generated-film, #header').animate({opacity: '1'}, 500);
			$('#generated-film, #header').removeClass('scale07');
		}, 500);
	}
	function hideFilm(){
		$('#generated-film, #header').animate({opacity: '0'}, 500);
		$('#generated-film, #header').addClass('scale07');
	}
});
