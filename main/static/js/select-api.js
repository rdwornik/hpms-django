//Retrive data from api
$("[data-url]").each(function(){
var $this = $(this);
var isTagsTrueSet = ($this.attr("tags") == "true")
  $this.select2({
    placeholder: "Select ".concat($this.attr("name")),
    allowClear : true,
    tags: isTagsTrueSet,
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
var query = new URLSearchParams(window.location.search)
var params = query.get($this.attr("name"))
if(params){
    $.ajax({
      type: 'GET',
      url: $this.attr("data-url").concat("?",query.toString())
  }).then(function (data) {
      // create the option and append to Select2
      console.log(params)
      var options = []
      if(data.count){
          data.results.forEach(element => options.push(new Option(element.text,element.id,false,true)))
      }else if(isTagsTrueSet){
          options.push(new Option(params,params,false,true))
      }
      $this.append(options).trigger('change');
      // manually trigger the `select2:select` event
      $this.trigger({
          type: 'select2:select',
          params: {
              data: data
          }
      });
  });
}
});

