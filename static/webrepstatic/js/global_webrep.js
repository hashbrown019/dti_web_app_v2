$onload(function(){
		var DATES = $CLASS('dates')
		for (var i = 0; i < DATES.length; i++) {
			DATES[i].innerText=date_readable(DATES[i].innerText,false)
		}
	})