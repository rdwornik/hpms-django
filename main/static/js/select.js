$("[url-endpoint-select]").select2({
  ajax:{
    url:function(){return this.attr("url-endpoint-select")},
    data: function(params){
      var query = {
        q: params.term,
      }
      return query;
    }
  }
});