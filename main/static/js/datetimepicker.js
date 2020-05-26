$('#id_time_0').datetimepicker({
    format:"Y-m-d H:i",
    onShow:function( ct ){
    this.setOptions({
    maxDate:$('#id_time_1').val()?$('#id_time_1').val():false
    })
    },
});
$('#id_time_1').datetimepicker({
    format:"Y-m-d H:i",
    onShow:function( ct ){
    this.setOptions({
    minDate:$('#id_time_0').val()?$('#id_time_0').val():false
    })
    },
});