$("[url-endpoint]").select2({
  ajax:{
    url:function(){return this.attr("url-endpoint")},
    data: function(params){
      var query = {
        q: params.term,
      }
      return query;
    }
  }
});