$(function(){
    $('.datetimepicker-input').val("");
    $('.datetimepicker-input').datetimepicker({
        format:"YYYY-MM-DD HH:mm",
        pick12HourFormat: false    
    });
});