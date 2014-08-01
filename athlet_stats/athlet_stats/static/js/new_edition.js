window.onload = function (){

	$('#datetimepicker1').datetimepicker({ language: 'es'});
  	
	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');

	function csrfSafeMethod(method) {
    	// these HTTP methods do not require CSRF protection
    	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});

	$("#id_modality").change(function(){
		if ( $("#id_modality option:selected").text() != "Otro"){
			$("#distance_container").fadeOut();
		}else{
			$("#distance_container").fadeIn();
		}
	})

	updateModality();


	$("#id_type").change(function(){
		updateModality();
	});



	function updateModality(){

		$.ajax({
		    url: '/changemodality/',
		    type: 'post',
		    data: {'race_type': $("#id_type").val()},
		    success: function(data) {
		    	$("#id_modality").html("");
		        for(var i=0; i<data.length; i++){
		        	$("#id_modality").append("<option id='"+data[i].pk+"'>"+data[i].fields.modality+"</option>");
		        }
		        if ( $("#id_modality option:selected").text() != "Otro"){
					$("#distance_container").fadeOut();
				}else{
					$("#distance_container").fadeIn();
				}
		    },
		    failure: function(data) { 
		        console.log(data);
		    }
		});

	}
	
}