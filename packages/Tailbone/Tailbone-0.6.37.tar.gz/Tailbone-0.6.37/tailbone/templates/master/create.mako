## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">New ${model_title}</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  ${self.disable_button_js()}
  % if dform is not Undefined:
      <% resources = dform.get_widget_resources() %>
      % for path in resources['js']:
          ${h.javascript_link(request.static_url(path))}
      % endfor
      % for path in resources['css']:
          ${h.stylesheet_link(request.static_url(path))}
      % endfor
  % endif
</%def>

<%def name="disable_button_js()">
  <script type="text/javascript">

    $(function() {

        $('form').submit(function() {
            var submit = $(this).find('input[type="submit"]');
            if (submit.length) {
                submit.button('disable').button('option', 'label', "Saving, please wait...");
            }
        });

    });
  </script>
</%def>

<%def name="context_menu_items()"></%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form-wrapper">
  ${form.render()|n}
</div><!-- form-wrapper -->
