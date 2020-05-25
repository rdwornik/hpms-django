// var $this = $(this);
//   $this.select2({
//     placeholder: "Select ".concat($this.attr("display-name")),
//     allowClear : true,
//     ajax:{
//       url: $this.attr("url-endpoint-select"),
//       data: function(params){
//         var query = {
//           q: params.term,
//         }
//         return query;
//       }
//     }
// });
// });


$("select").each(function(){
  var $this = $(this);
  $this.select2({
    placeholder: "Select ".concat($this.attr("name")),
    });
});
