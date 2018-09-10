$('#tSelect').change(function(){
    selectV = $('#tSelect').val();
    cond = $('#conditions');
    act = $('#actions');
    if(selectV==-1){
        cond.empty();
        act.empty();
    }
    if(selectV==0){
        $.getJSON( "/diagnostics/rules/help/ddmr/", function( data ) {
            cond.empty();
            act.empty();
            cond.conditionsBuilder(data);
            act.actionsBuilder(data);
        });
    }
    if(selectV==1){
        $.getJSON( "/diagnostics/rules/help/padr/", function( data ) {
            cond.empty();
            act.empty();
            cond.conditionsBuilder(data);
            act.actionsBuilder(data);
        });
    }
    if(selectV==2){
        $.getJSON( "/diagnostics/rules/help/fdsr/", function( data ) {
            cond.empty();
            act.empty();
            cond.conditionsBuilder(data);
            act.actionsBuilder(data);
        });
    }
    if(selectV==3){
        $.getJSON( "/diagnostics/rules/help/ddbosr/", function( data ) {
            cond.empty();
            act.empty();
            cond.conditionsBuilder(data);
            act.actionsBuilder(data);
        });
    }
    if(selectV==4){
        $.getJSON( "/diagnostics/rules/help/mar/", function( data ) {
            cond.empty();
            act.empty();
            cond.conditionsBuilder(data);
            act.actionsBuilder(data);
        });
    }
    if(selectV==5){
        $.getJSON( "/diagnostics/rules/help/rfgp/", function( data ) {
            cond.empty();
            act.empty();
            cond.conditionsBuilder(data);
            act.actionsBuilder(data);
        });
    }
});

$('#confirmNew').submit(function(e) {
    $('#cont').val(JSON.stringify({'conditions':$('#conditions').conditionsBuilder("data"),'actions':$('#actions').actionsBuilder("data")}));
    return true;
});