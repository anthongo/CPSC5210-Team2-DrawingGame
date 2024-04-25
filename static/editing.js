var username;

function setup(show_comment) {
    function deletePost(){
        $( "#dialog-confirm" ).dialog({
        resizable: false,
        height: "auto",
        width: 400,
        modal: true,
        buttons: {
            "Delete": function() {
                $.post(window.location.href, {"delete-post": true}).done(function(data){
                    window.location.href="/user/"+username;
                });
                $( this ).dialog( "close" );
            },
            Cancel: function() {
                $( this ).dialog( "close" );
            }
        }
        });
    }

    $( "#dialog-confirm" ).hide();
    $('#delete-post').click(deletePost);
    $('.pure-button.alert-btn.alert-error').click(deletePost);
    $('#editing-see-guesses').prop('checked', show_comment);
}