function cadastrarLocal(local){
	$.ajax({
		method : 'POST',
		url : 'http://localhost:5000/locais',
		data : local
	}).done(function(resposta){
		console.log(resposta);
	});
}

function atualizarLocal(local){
	$.ajax({
		method : 'PUT',
		url : 'http://localhost:5000/locais/'+local.local_id,
		data : JSON.stringify(local)
	}).done(function(resposta){
		console.log(resposta);
	});
}

function listarLocais(){
	$.ajax({
		method : 'GET',
		url : 'http://localhost:5000/locais'
	}).done(function(resposta){
		console.log(resposta);
	});
}

function consultarLocal(id){
	$.ajax({
		method : 'GET',
		url : 'http://localhost:5000/locais/' + id
	}).done(function(resposta){
		console.log(resposta);
	}).fail(function(resposta){
		console.log(resposta);
	});
}