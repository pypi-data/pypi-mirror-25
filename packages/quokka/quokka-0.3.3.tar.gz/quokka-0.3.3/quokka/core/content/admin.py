# from flask_admin.helpers import get_form_data
import datetime as dt

from flask import current_app
from quokka.admin.forms import ValidationError
from quokka.admin.views import ModelView
from quokka.core.auth import get_current_user
from quokka.utils.routing import get_content_url
from quokka.utils.text import slugify

from .formats import CreateForm, get_format


class ContentView(ModelView):
    """Base form for all contents"""
    details_modal = True
    can_view_details = True
    create_modal = True
    # can_export = True
    # export_types = ['csv', 'json', 'yaml', 'html', 'xls']

    # details_modal_template = 'admin/model/modals/details.html'
    # create_template = 'admin/model/create.html'

    # edit_template = 'admin/quokka/edit.html'
    # EDIT template is taken from content_format

    page_size = 20
    can_set_page_size = True

    form = CreateForm
    column_list = (
        'title',
        'category',
        'authors',
        'date',
        'modified',
        'language',
        'published'
    )

    column_sortable_list = (
        'title',
        'category',
        'authors',
        'date',
        'modified',
        'language',
        'published'
    )
    column_default_sort = ('date', True)

    # TODO: implement scaffold_list_form in base class to enable below
    # column_editable_list = ['category', 'published', 'title']

    column_details_list = [
        'title',
        'category',
        'slug',
        'content_format',
        'content_type',
        'language',
        'date',
        'created_by',
        'modified',
        'modified_by',
        'version',
        '_isclone',
        'quokka_module',
        'quokka_format_module',
        'quokka_format_class',
        'quokka_create_form_module',
        'quokka_create_form_class'
    ]

    # column_export_list = []
    # column_formatters_export
    # column_formatters = {fieldname: callable} - view, context, model, name

    # column_extra_row_actions = None
    """
        List of row actions (instances of :class:`~flask_admin.model.template.
        BaseListRowAction`).

        Flask-Admin will generate standard per-row actions (edit, delete, etc)
        and will append custom actions from this list right after them.

        For example::

            from flask_admin.model.template import EndpointLinkRowAction,
            LinkRowAction

            class MyModelView(BaseModelView):
                column_extra_row_actions = [
                    LinkRowAction('glyphicon glyphicon-off',
                    'http://direct.link/?id={row_id}'),
                    EndpointLinkRowAction('glyphicon glyphicon-test',
                    'my_view.index_view')
                ]
    """

    # form_edit_rules / form_create_rules
    # form_rules = [
    #     # Define field set with header text and four fields
    #     rules.FieldSet(('title', 'category', 'tags'), 'Base'),
    #     # ... and it is just shortcut for:
    #     rules.Header('Content Type'),
    #     rules.Field('summary'),
    #     rules.Field('date'),
    #     # ...
    #     # It is possible to create custom rule blocks:
    #     # MyBlock('Hello World'),
    #     # It is possible to call macros from current context
    #     # rules.Macro('my_macro', foobar='baz')
    # ]

    # def create_form(self):
    #     form = super(ContentView, self).create_form()
    #     form.content_type.choices = [('a', 'a'), ('b', 'b')]
    #     return form

    # @property
    # def extra_js(self):
    #     return [
    #         url_for('static', filename='js/quokka_admin.js')
    #     ]

    def edit_form(self, obj):
        content_format = get_format(obj)
        self.edit_template = content_format.get_edit_template(
            obj
        ) or self.edit_template
        self.form_edit_rules = content_format.get_form_rules()
        self._refresh_form_rules_cache()
        form = content_format.get_edit_form(obj)
        return form

    def on_form_prefill(self, form, id):
        """Fill edit form with versioned data"""
        form.content.data = current_app.db.pull_content(id)

    def get_save_return_url(self, model, is_created):
        if is_created:
            return self.get_url('.edit_view', id=model['_id'])
        return super(ContentView, self).get_save_return_url(model, is_created)

    def on_model_change(self, form, model, is_created):

        if is_created:
            # each custom module should be identified by admin and format class
            self.add_module_metadata(model)

        get_format(model).before_save(form, model, is_created)

        if not model.get('slug'):
            model['slug'] = slugify(model['title'])

        existent = current_app.db.get('index', {'slug': model['slug'],
                                                'category': model['category']})

        if (is_created and existent) or (
                existent and existent['_id'] != model['_id']):
            raise ValidationError(f'{get_content_url(model)} already exists')

        now = dt.datetime.now()
        current_user = get_current_user()

        if is_created:
            # this defaults are also applied for cloning action
            model['date'] = now
            model['created_by'] = current_user
            model['_id'] = current_app.db.generate_id()
            model['language'] = current_app.config.get(
                'BABEL_DEFAULT_LOCALE', 'en'
            )
            model['published'] = False
            model['modified'] = None
            model['modified_by'] = None

        model['modified'] = now
        model['modified_by'] = current_user

        model.pop('csrf_token', None)

        current_app.db.push_content(model)

    def after_model_change(self, form, model, is_created):
        get_format(model).after_save(form, model, is_created)

    def add_module_metadata(self, model):
        quokka_format = get_format(model)
        form = getattr(self.__class__, 'form', self.get_form())
        model['quokka_module'] = self.__module__
        model['quokka_format_module'] = quokka_format.__module__
        model['quokka_format_class'] = quokka_format.__class__.__name__
        model['quokka_create_form_module'] = form.__module__
        model['quokka_create_form_class'] = form.__class__.__name__
