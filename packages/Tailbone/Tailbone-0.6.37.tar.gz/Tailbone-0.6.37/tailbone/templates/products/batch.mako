## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="title()">Products: Create Batch</%def>

<%def name="context_menu_items()">
  <li>${h.link_to("Back to Products", url('products'))}</li>
</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">
    $(function() {

        $('#batch_type').selectmenu({
            change: function(event, ui) {
                $('.params-wrapper').hide();
                $('.params-wrapper.' + ui.item.value).show();
            }
        });

        $('.params-wrapper.' + $('#batch_type').val()).show();

        $('#make-batch').click(function() {
            $(this).button('disable').button('option', 'label', "Working, please wait...");
            $(this).parents('form:first').submit();
        });

    });
  </script>
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  <style type="text/css">
    .params-wrapper {
        display: none;
    }
  </style>
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form">
  ${h.form(request.current_route_url())}
  ${h.csrf_token(request)}

  ${self.wtfield(form, 'batch_type')}

  % for key, pform in params_forms.items():
      <div class="params-wrapper ${key}">
        % for name in pform._fields:
            ${self.wtfield(pform, name)}
        % endfor
      </div>
  % endfor

  <div class="buttons">
    <button type="button" id="make-batch">Create Batch</button>
    ${h.link_to("Cancel", url('products'), class_='button')}
  </div>

  ${h.end_form()}
</div>
