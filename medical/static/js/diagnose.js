$('#testAlergy').click(function(){
    $('#testFaild').show(200);
});

$('#detectDisease').click(function(){
    $.getJSON('autodiagnose/',{'rules':$('#rules').val(),'patient':$('#patient').val(),'hadTemp':$('#hadTemp').val(),'temp':$('#temp').val(),'symptoms':$('#symptoms').val()},function(data){
        $('#detectionResult').empty();
        $('#detectionResult').append("<strong>Desease:</strong>\t"+data.disease+" \t<strong>Probability:</strong>\t"+data.probability+"%");
        $('#diseaseTestResults').show(200);
    });
    
});

$('#hadTemp').change(function(){
    if(this.checked) {
        $(this).prop("value", 'True');
    }else{
        $(this).prop("value", 'False');
    }
    
});

$('#synSelect').change(function(){
    $("#symptoms").val($("#synSelect").val());
    return true;
});
$('#ruleSelect').change(function(){
    $("#rules").val($("#ruleSelect").val());
    return true;
});
$('#medSelect').change(function(){
    $("#medicines").val($('#medSelect').val());
    return true;
});

$('#testAlergy').click(function(){
    $.getJSON('alergy/',{'medicines':$('#medicines').val(),'patient':$('#patient').val()},function(data){
        if(data.alarm){
            $('#testPassed').hide();
            $('#testFaild').hide();
            $('#testFaild').show(200);
        }else{
            $('#testPassed').hide();
            $('#testFaild').hide();
            $('#testPassed').show(200);
        }
    });
    
});

$('#posibleDisList').click(function(){
    window.location.href = "diseases/?symptoms="+$('#symptoms').val();
});