## -*- coding: utf-8; -*-
<%inherit file="/batch/index.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">

    var has_execution_options = ${'true' if master.has_execution_options(batch) else 'false'};

    $(function() {

        $('#execute-results-button').click(function() {
            var form = $('form[name="execute-results"]');
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
                                dialog_button(event).button('option', 'label', "Executing, please wait...").button('disable');
                                form.submit();
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
                form.submit();
            }
        });

    });

  </script>
</%def>

<%def name="grid_tools()">
  % if request.has_perm('batch.handheld.execute_results'):
      <button type="button" id="execute-results-button">Execute Results</button>
  % endif
</%def>

${parent.body()}

<div id="execution-options-dialog" style="display: none;">
  ${h.form(url('{}.execute_results'.format(route_prefix)), name='execute-results')}
  ${h.csrf_token(request)}
  <br />
  <p>
    Please be advised, you are about to execute multiple batches!&nbsp; They will
    be aggregated and treated as a single data source, during execution.
  </p>
  <br />
  % if master.has_execution_options(batch):
      ${rendered_execution_options|n}
  % endif
  ${h.end_form()}
</div>
