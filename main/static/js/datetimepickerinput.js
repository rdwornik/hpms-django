$(function(){
    $('.datetimepicker-input').val("");
    $('.datetimepicker-input').datetimepicker({
        format:"DD/MM/YYYY HH:mm",
        pick12HourFormat: false    
    });
});