$("[autocomplete]").each(function(){
    var $this = $(this);
    $this.autocomplete({
        source: function( request, response ) {
          $.ajax( {
            url: $this.attr("data-url"),
            dataType: "json",
            data: {
              term: request.term
            },
            success: function( data ) {
              response( data );
            }
          });
        },
        minLength: 0
      }).focus(function(){
        $this.data("uiAutocomplete").search($this.val());
      });    
})