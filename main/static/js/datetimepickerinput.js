$(function(){
    $('.datetimepicker-input').val("")
    $('.datetimepicker-input').datetimepicker({
        format:"YYYY-MM-DD HH:mm",
        pick12HourFormat: false,
    });
    $('.datetimepicker-input').val(function(){return this.attributes.getNamedItem("value").value });
});