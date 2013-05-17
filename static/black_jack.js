/**
 * Created with PyCharm.
 * User: hurle1s
 * Date: 5/7/13
 * Time: 9:14 AM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function(){
    console.log("TESTING")
    $('#id_bet').change(function(){

        $.get('/game/bet/?bet='+$('#id_bet').val(), function(data){
        }).success(function(){
                console.log("success")
                $('#start_game_button').removeAttr('disabled');
            });
    });
});