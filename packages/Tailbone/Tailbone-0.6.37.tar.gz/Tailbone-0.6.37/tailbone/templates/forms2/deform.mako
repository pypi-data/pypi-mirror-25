## -*- coding: utf-8; -*-

% if not readonly:
<% _focus_rendered = False %>
${h.form(form.action_url, id=dform.formid, method='post', enctype='multipart/form-data')}
${h.csrf_token(request)}
% endif

##   % for error in fieldset.errors.get(None, []):
##       <div class="fieldset-error">${error}</div>
##   % endfor

% for field in form.fields:

    ## % if readonly or field.name in readonly_fields:
    % if readonly:
        ${render_field_readonly(field)|n}
    % elif field not in dform and field in form.readonly_fields:
        ${render_field_readonly(field)|n}
    % elif field in dform:
        <% field = dform[field] %>

    ##       % if field.requires_label:
            <div class="field-wrapper ${field.name} ${'error' if field.error else ''}">
    ##             % for error in field.errors:
    ##                 <div class="field-error">${error}</div>
    ##             % endfor
              % if field.error:
                  <div class="field-error">${field.error.msg}</div>
              % endif
              <label for="${field.oid}">${field.title}</label>
              <div class="field">
                ${field.serialize()|n}
              </div>
    ##             % if 'instructions' in field.metadata:
    ##                 <span class="instructions">${field.metadata['instructions']}</span>
    ##             % endif
            </div>

            ## % if not _focus_rendered and (fieldset.focus is True or fieldset.focus is field):
            % if not readonly and not _focus_rendered:
                ## % if not field.is_readonly() and getattr(field.renderer, 'needs_focus', True):
                % if not field.widget.readonly:
                    <script type="text/javascript">
                      $(function() {
    ##                       % if hasattr(field.renderer, 'focus_name'):
    ##                           $('#${field.renderer.focus_name}').focus();
    ##                       % else:
    ##                           $('#${field.renderer.name}').focus();
    ##                       % endif
                          $('#${field.oid}').focus();
                      });
                    </script>
                    <% _focus_rendered = True %>
                % endif
            % endif

    ##       % else:
    ##           ${field.render()|n}
    ##       % endif

    % endif

% endfor

% if buttons:
    ${buttons|n}
% elif not readonly:
    <div class="buttons">
      ## ${h.submit('create', form.create_label if form.creating else form.update_label)}
      ${h.submit('save', "Save")}
##         % if form.creating and form.allow_successive_creates:
##             ${h.submit('create_and_continue', form.successive_create_label)}
##         % endif
      ${h.link_to("Cancel", form.cancel_url, class_='button autodisable')}
    </div>
% endif

% if not readonly:
${h.end_form()}
% endif
