//Retrive data from api
$("[data-url]").each(function(){
var $this = $(this);
  $this.select2({
    placeholder: "Select ".concat($this.attr("name")),
    allowClear : true,
    ajax:{
      url: $this.attr("data-url"),
      data: function(params){
        var query = {
          q: params.term,
        }
        return query;
      }
    }
});
//Set query parameters
query = new URLSearchParams(window.location.search)
params = query.get($this.attr("name"))
if(params){
    var ipSelect=$("[data-url]")
    $.ajax({
      type: 'GET',
      url: ipSelect.attr("data-url").concat("?",query.toString())
  }).then(function (data) {
      // create the option and append to Select2
      console.log(data)
      var options = []
      data.results.forEach(element => options.push(new Option(element.text,element.id,false,true)))
      ipSelect.append(options).trigger('change');

      // manually trigger the `select2:select` event
      ipSelect.trigger({
          type: 'select2:select',
          params: {
              data: data
          }
      });
  });
}
});

