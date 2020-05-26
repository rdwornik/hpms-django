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
params = query.getAll($this.attr("name"))
if(params){
  var options = []
  params.forEach(element => options.push(new Option(element,element,false,true)))
  $("#id_".concat($this.attr("name"))).append(options).trigger("change");
}
});

