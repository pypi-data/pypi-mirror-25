
/************************************************************
 *
 * tailbone.batch.js
 *
 * Common logic for view/edit batch pages
 *
 ************************************************************/


$(function() {
    
    $('.grid-wrapper').gridwrapper();

    $('#execute-batch').click(function() {
        if (has_execution_options) {
            $('#execution-options-dialog').dialog({
                title: "Execution Options",
                width: 500,
                height: 300,
                modal: true,
                buttons: [
                    {
                        text: "Execute",
                        click: function(event) {
                            $(event.target).button('option', 'label', "Executing, please wait...").button('disable');
                            $('form[name="batch-execution"]').submit();
                        }
                    },
                    {
                        text: "Cancel",
                        click: function() {
                            $(this).dialog('close');
                        }
                    }
                ]
            });
        } else {
            $(this).button('option', 'label', "Executing, please wait...").button('disable');
            $('form[name="batch-execution"]').submit();
        }
    });

});
