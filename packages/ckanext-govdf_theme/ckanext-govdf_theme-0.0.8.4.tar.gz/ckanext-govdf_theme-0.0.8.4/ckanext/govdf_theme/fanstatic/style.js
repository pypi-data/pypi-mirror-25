jQuery(function($){
	/*
	* Aciona a funcionalidade do campo de busca do menu principal.
	*/
	$('#header-search-trigger').click(function(){
		$('#header-search-input').toggleClass('search-input-open');
		$('.head-area-busca').toggleClass('head-area-busca-open');
	});
	$(document).click(function(e){
		if(!$(e.target).closest('.ngen-search-form').length){
			$('#header-search-input').removeClass('search-input-open');
			$('.head-area-busca').removeClass('head-area-busca-open');
		}
	});

	/*
	* Aciona a funcionalidade do accordion na página de perguntas e respostas.
	*/
	$('#perguntas a').click(function(){
		if($('#perguntas a').hasClass('collapsed')){
	    	$('#perguntas a.collapsed').prev().prev().removeClass('panel-heading-active');
	    }
	    else{
	    	$('#perguntas a').prev().prev().addClass('panel-heading-active');
	    }
	});

	/*
	* Aciona as funcionalidades de adaptação dos tamanhos das caixas de temas e de fontes de dados.
	*/
	$( document ).ready(function() {
		home_resize_theme_box();
		organization_resize_organization_box();
    $('.collapse').collapse();
  	$('.dropdown-toggle').dropdown()
	});
});

/*
* Readaptação dos tamanhos das caixas de temas.
*/
var home_resize_theme_box = function(){
	var boxes = $("#themes-module .group-item-conainter").length;

	if ((boxes % 4) == 3){
		$("#themes-module .group-item-conainter").first().removeClass('col-md-3').addClass('col-md-6');
	}
	else if ((boxes % 4) == 2) {
		$("#themes-module .group-item-conainter").first().removeClass('col-md-3').addClass('col-md-6');
		$("#themes-module .group-item-conainter").last().removeClass('col-md-3').addClass('col-md-6');
	}
	else if ((boxes % 4) == 1) {
		$("#themes-module .group-item-conainter").first().removeClass('col-md-3').addClass('col-md-6');
		$("#themes-module .group-item-conainter").eq(1).removeClass('col-md-3').addClass('col-md-6');
		$("#themes-module .group-item-conainter").eq(-2).removeClass('col-md-3').addClass('col-md-6');
		if (boxes == 1) {
			$("#themes-module .group-item-conainter").addClass('col-md-offset-3');
		}
	}
}

/*
* Readaptação dos tamanhos das caixas de fontes de dados.
*/
var organization_resize_organization_box = function(){
	var h = 0;
	$(".organization-item").each(function() {
		if (h < $(this).outerHeight()) {
			h = $(this).outerHeight();
		}
  });
	$(".organization-item").css("height",h);
}


/** modificando os valores referentes ao font-size */
var siteBase = "http://127.0.0.1:5000";
var acessibilidadeContraste;
var acessibilidadeFontSize = typeof acessibilidadeFontSize != 'undefined' ? acessibilidadeFontSize : 4;
var elAcessibilidade = new Array();

$("h1, h2, h3, h4, h5, p, a, li").each(function(i, el) {
		elAcessibilidade.push({'el': el, 'value':$(this).css('font-size')});
});

$(document).on("change", "#sizeFont", function() {
		var value = $(this).val();
		acessibilidadeFontSize=value;
		acessibilidade(value);
		$.post(siteBase, {'acessibilidade': 1, 'acessibilidade_font': value}, function(r) {console.log(r)})
});

$(document).on("click", '#checkboxAcessibilidade', function() {
		var checked = $(this).is(":checked");
		if (checked) {
				acessibilidadeContraste=1;
				$('body').prepend('<link id="styleAcessibilidade" href="/../css/theme_acessivel.css" rel="stylesheet" type="text/css"/>');
				$(".info-contraste").html('Alto contraste ligado');
				$.post(siteBase, {acessibilidade: 1, acessibilidade_contraste: 1}, function(r) {console.log(r)});
		} else {
				acessibilidadeContraste=0;
				$("#styleAcessibilidade").remove();
				$(".info-contraste").html('Alto contraste desligado');
				$.post(siteBase, {acessibilidade: 1, acessibilidade_contraste: 0}, function(r) {console.log(r)});
		}
 });

/**
 * Função que aumenta|reduz a fonte da página, muda o contraste do site.
 *
 * @param {string}
 */
function acessibilidade(novoValor){
		soma = (novoValor < 4) ? ((((4-novoValor)*-1)*2)) : ((novoValor > 4) ?((novoValor-4)*2) : 0);

		for (var i in elAcessibilidade) {
				$(elAcessibilidade[i].el).css('font-size', (parseInt(elAcessibilidade[i].value.replace('px', ''))+soma)+'px')
		}
}

$('#popoverAcessibilidade').popover({
	html: true,
	content: '<div class="cntAcessibilidade">'+
				 '<div class="titulo">Tamanho de fonte</div>'+
				 '<div class="aMenor">A</div>'+
				 '<div class="ranger"><input type="range" id="sizeFont" min="1" max="8" value="4" step="1" /></div>'+
				 '<div class="aMaior">A</div>'+
				 '<div class="clearfix"></div>'+
				 '<div class="bg-verde">'+
						'<div class="areacheckbox">'+
							'<div class="checkboxCampoInterno">'+
								'<input type="checkbox" value="1" id="checkboxAcessibilidade" name="" '+ ((typeof acessibilidadeContraste != 'undefined' && acessibilidadeContraste == 1) ? 'checked' : '') +' />'+
								'<label for="checkboxAcessibilidade"></label>'+
							'</div>'+
						'</div>'+
						'<div class="info-contraste">Alto contraste '+ ((typeof acessibilidadeContraste != 'undefined' && acessibilidadeContraste == 1) ? 'ligado' : 'desligado') +'</div>'+
				 '</div>'+
			 '</div>'
}).click(function() {
	$(".cntAcessibilidade").parents('.popover-content').css({"padding": "9px 0px 0px 0px"}).parents(".popover").css({"padding" : "0px"});
	$("#checkboxAcessibilidade").prop('checked', (typeof acessibilidadeContraste != 'undefined' && acessibilidadeContraste == 1));
	$(".info-contraste").html('Alto contraste '+ ((typeof acessibilidadeContraste != 'undefined' && acessibilidadeContraste == 1) ? 'ligado' : 'desligado'));
	$("#sizeFont").val(acessibilidadeFontSize);
});
$('body').on('click', function (e) {
		$('[data-toggle="popover"]').each(function () {
				if (!$(this).is(e.target) && $(this).has(e.target).length === 0 || $('.popover').has(e.target).length === 0) {
						$(this).popover('hide');
				}
		});
});
