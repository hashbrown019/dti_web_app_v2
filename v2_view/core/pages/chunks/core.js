$onload(function(){
	if("alert"in URL_ARGS){
		var _alert = URL_ARGS["alert"].split(":")
		var alert_card = (`
			<div class="x-col x-right l3 alert alert-${_alert[0]} alert-dismissible fade show" role="alert" style="right: 1vw;bottom:10vh ;position: fixed; z-index: 10;">
				<b>${_alert[1]}</b>
				<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
			</div>
		`)
		$ID("alert_float_holder").innerHTML = alert_card
	}
})



function show_container_by_class(clname){
	var CDCARDS = $CLASS(clname)
	return{
		show : function(indx){
			for (var i = 0; i < CDCARDS.length; i++) {
				if (i==indx) {CDCARDS[i].style.display="block"}
				else{CDCARDS[i].style.display="none"}
			}
			return CDCARDS[indx]
		}
	}
}


function personal_form_range_action(elem,field_name){
	elem.parentNode.querySelectorAll("label.f_name")[0].innerHTML=field_name + "<i> Current Value: <b>" +elem.value + "</b></i>";
}

// $onload(check_DD_FROM_DB)
function remove_DD_FROM_DB_opt(){
	var DD_FROM_DB = $CLASS("DD_FROM_DB")
	for (var i = 0; i < DD_FROM_DB.length; i++) {
		DD_FROM_DB[i].innerHTML = ""
	}
}


function check_DD_FROM_DB(){
	var DD_FROM_DB = $CLASS("DD_FROM_DB")
	var reqs = []
	for (var i = 0; i < DD_FROM_DB.length; i++) {
		reqs.push([
			DD_FROM_DB[i].getAttribute('_db_table'),
			DD_FROM_DB[i].getAttribute('_db_col'),
			DD_FROM_DB[i].id
		]);
	}
	gettable_data(reqs,reqs.length-1)
}

function gettable_data(reqs,l_index){
	$send({
		action : "/mis-v4/personal-forms/get-db-col",
		method : POST,
		data : $DATA({"_db_table":reqs[l_index][0] ,"_db_col":reqs[l_index][1]}),
		func : function(r){
			var opt = ""
			var res = JSON.parse(r);
			for (var i = 0; i < res.length; i++) {
				var opt_str = ""+res[i]['col']
				if(opt_str.length >0){
					opt +=(`<option value="${res[i]['col']}||R-ID${res[i]['id']}">${res[i]['col']}</option>`)
				}
			}
			$ID(reqs[l_index][2]).innerHTML = opt

			if(l_index <=0  ){
			}else{
				l_index -=1
				gettable_data(reqs,l_index) // CALL ITS SELF
			}
		}
	})
}


// ================================
function EMBED__SCRIPT(obj,func=function(args,arg2){}) {
	var EMBED_STACK = obj.contentWindow
	var EMBED_DOC = EMBED_STACK.document.documentElement
	obj.style.height = EMBED_DOC.scrollHeight + 'px';

	var EMBED_EXCLUDE = EMBED_DOC.getElementsByClassName('EMBED_EXCLUDE')
	for (var i = 0; i < EMBED_EXCLUDE.length; i++) {
		EMBED_EXCLUDE[i].style.display='none'
	}
	// println(obj)
	// println(EMBED_STACK)
	// println(EMBED_STACK.swal)
	// EMBED_STACK.swal = alert
	// println(EMBED_STACK.swal)

	// var allRows = document.querySelectorAll('.row[id]');
	// allRows.forEach(function(row) {
	// 	row.style.display = 'flex';
	// });
	func(EMBED_DOC,obj)
}

function EMBED_LOAD_START(){
	alert()
}
