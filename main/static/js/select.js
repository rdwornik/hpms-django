$(".django-form").find("select").each(function(){
  var $this = $(this);
  $this.select2({
    placeholder: "Select ".concat($this.attr("name")),
    allowClear : true
    });
});