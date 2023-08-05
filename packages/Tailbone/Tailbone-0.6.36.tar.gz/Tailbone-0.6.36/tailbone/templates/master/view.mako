## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="title()">${model_title_plural} &raquo; ${instance_title}</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  % if master.has_rows:
      ${h.javascript_link(request.static_url('tailbone:static/js/jquery.ui.tailbone.js'))}
      <script type="text/javascript">
        $(function() {
            $('.grid-wrapper').gridwrapper();
        });
      </script>
  % endif
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  % if master.has_rows:
      <style type="text/css">
        .grid-wrapper {
            margin-top: 10px;
        }
      </style>
  % endif
</%def>

<%def name="content_title()">
  % if master.supports_prev_next:
      <div style="float: right;">
        % if prev_instance:
            ${h.link_to(u"« Older", url('{}.view'.format(route_prefix), uuid=prev_instance.uuid), class_='button autodisable')}
        % else:
            ${h.link_to(u"« Older", '#', class_='button', disabled='disabled')}
        % endif
        % if next_instance:
            ${h.link_to(u"Newer »", url('{}.view'.format(route_prefix), uuid=next_instance.uuid), class_='button autodisable')}
        % else:
            ${h.link_to(u"Newer »", '#', class_='button', disabled='disabled')}
        % endif
      </div>
  % endif
  <h1>${instance_title}</h1>
</%def>

<%def name="context_menu_items()">
  <li>${h.link_to("Permalink for this {}".format(model_title), action_url('view', instance))}</li>
  % if master.has_versions and request.rattail_config.versioning_enabled() and request.has_perm('{}.versions'.format(permission_prefix)):
      <li>${h.link_to("Version History", action_url('versions', instance))}</li>
  % endif
  % if master.editable and instance_editable and request.has_perm('{}.edit'.format(permission_prefix)):
      <li>${h.link_to("Edit this {}".format(model_title), action_url('edit', instance))}</li>
  % endif
  % if master.deletable and instance_deletable and request.has_perm('{}.delete'.format(permission_prefix)):
      <li>${h.link_to("Delete this {}".format(model_title), action_url('delete', instance))}</li>
  % endif
  % if master.creatable and request.has_perm('{}.create'.format(permission_prefix)):
      <li>${h.link_to("Create a new {}".format(model_title), url('{}.create'.format(route_prefix)))}</li>
  % endif
  % if master.cloneable and request.has_perm('{}.clone'.format(permission_prefix)):
      <li>${h.link_to("Clone this as new {}".format(model_title), url('{}.clone'.format(route_prefix), uuid=instance.uuid))}</li>
  % endif
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form-wrapper">
  ${form.render()|n}
</div><!-- form-wrapper -->

% if master.has_rows:
    ${rows_grid|n}
% endif
