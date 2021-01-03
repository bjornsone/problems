$( function() {
    $( "#dialog_of_links" ).dialog({
      modal: true,
      width: 700,
      autoOpen: false,
      buttons: {
        Ok: function() {
          $( this ).dialog( "close" );
        }
      }
    });
} );

var getAbsoluteUrl = (function() {
    //Thanks to https://davidwalsh.name/get-absolute-url
	var a;

	return function(url) {
		if(!a) a = document.createElement('a');
		a.href = url;

		return a.href;
	};
})();

$('#link_to_dialog').click(function() {
    $('#qa_link').val(window.location.href)
    $('#q_link').val(getAbsoluteUrl('{{redirect_path}}?{{params['no_answer']}}'))
    $('#dialog_of_links').dialog('open');
    console.log(getAbsoluteUrl('test'));
    return false;
});