$(function() {
	let film = {
		img: $('.generated-film__info--img img'),
		title: $('.generated-film__info--detail .title'),
		overview: $('.generated-film__overview'),
		genre: $('.generated-film__info--detail .genre'),
		runtime: $('.generated-film__info--detail .runtime .time'),
		countries: $('.generated-film__info--detail .runtime .countries'),
		releaseDate: $('.generated-film__info--detail .runtime .release-date'),
		voteCount: $('.generated-film__info--detail .ratings .votes .bot'),
		voteAverage: $('.generated-film__info--detail .ratings .votes .top'),
		popularity: $('.generated-film__info--detail .ratings .rating .top'),
		backdrop: $('.generated-film__backdrop'),


		show: function(data){
			film.img.attr('src', 'https://image.tmdb.org/t/p/w500/' + data.poster_path);
			film.backdrop.css({'background-image':  'url(https://image.tmdb.org/t/p/original/' + data.backdrop_path + ')'});
			film.title.html(data.title);
			film.releaseDate.html(data.release_date.split('-')[0]);
			film.overview.html(data.overview);
			film.voteCount.html(data.vote_count + ' голосов');
			film.voteAverage.html(data.vote_average * 10 + '%');
			film.popularity.html(data.popularity);

			let runtime = Math.floor(data.runtime / 60) + 'h ' + data.runtime % 60 + 'm';
			film.runtime.html(runtime);

			let genres = '';
			for(let i = 0; i < data.genres.length; i++){
				genres += data.genres.length == 1 || i == data.genres.length-1 ? data.genres[i].name : data.genres[i].name + ', '
			}
			film.genre.html(genres);


			let countries = '';
			for(let i = 0; i < data.production_countries.length; i++){
				countries += data.production_countries.length == 1 || i == data.production_countries.length-1 ? data.production_countries[i].iso_3166_1 : data.production_countries[i].iso_3166_1 + ', '
			}
			film.countries.html(countries);


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
