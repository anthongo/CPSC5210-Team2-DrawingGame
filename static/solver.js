$("#dialog-confirm").hide();
function noHintProvided() {
    $("#dialog-text").text(`The author did not provide a hint.`)
    $("#dialog-confirm").dialog({
        title: "No hint",
        resizable: false,
        height: "auto",
        width: 400,
        modal: true,
        buttons: {
            Cancel: function () {
                $(this).dialog("close");
            }
        }
    });
}

function hintProvided() {
    $("#solver_actual_hint").hide()
    $("#dialog-text").text(`Do you really want to see the hint?`)
    $("#dialog-confirm").dialog({
        title: "Hint Confirmation",
        resizable: false,
        height: "auto",
        width: 400,
        modal: true,
        buttons: {
            "Yes": function () {
                $("#dialog-text").text(``)
                $("#solver_actual_hint").show()
                $(this).dialog({
                    title: "Author's hint",
                    resizable: false,
                    height: "auto",
                    width: 400,
                    modal: true,
                    buttons: {
                        Close: function () {
                            $(this).dialog("close");
                        }
                    }
                });
            },
            "No": function () {
                $(this).dialog("close");
            }
        }
    });
}

function comment_more_setting(comment_id) {
    $("#dialog-text").text(`Are you sure you want to delete this comment?`)
    $("#dialog-confirm").dialog({
        title: "Delete comment?",
        resizable: false,
        height: "auto",
        width: 400,
        modal: true,
        buttons: {
            "Yes": function() {
                $.ajax({
                    type: 'POST',
                    url: "/post/deleteComment/",
                    data: {
                        'comment_id': comment_id
                    }
                })
                .done(function( msg ) {
                  if(msg == "Success"){
                    $("#solver_each_user_all_data_"+comment_id).remove()
                  } else {
                    alert("Deleting comment unsuccessful!");
                  }
                });
                $( this ).dialog( "close" );
            },
            Cancel: function () {
                $(this).dialog("close");
            }
        }
    });
}
function comment_more_setting_answer(comment_id) {
    $("#dialog-text").text(`You cannot delete this comment since this is the answer.`)
    $("#dialog-confirm").dialog({
        title: "Can't delete solution",
        resizable: false,
        height: "auto",
        width: 400,
        modal: true,
        buttons: {
            Close: function () {
                $(this).dialog("close");
            }
        }
    });
}

function setupComments(solved, show_comment) {
    if (solved) {
        $(".solver_other_user_answers").hide();
        $('#toggleComments span').text("Show")
    }

    if (show_comment) {
        $('#toggleComments').click(function(){
            $('.solver_other_user_answers').slideToggle('slow');
            $('.rotate').toggleClass("down");
            if  ($('.rotate').hasClass("down")) {
                $('#toggleComments span').text("Hide")
            }       
            else {
                $('#toggleComments span').text("Show")
            }   
        });
    }
}