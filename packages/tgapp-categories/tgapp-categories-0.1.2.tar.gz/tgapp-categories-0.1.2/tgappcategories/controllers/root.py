# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate, predicates
from tg.i18n import ugettext as _

from tgappcategories import model
from tgext.pluggable import app_model, plug_url, plug_redirect

from tgappcategories.lib import get_new_category_form, get_edit_category_form


class RootController(TGController):
    allow_only = predicates.has_permission('tgappcategories')

    @expose('tgappcategories.templates.index')
    def index(self):
        categories = model.provider.query(model.Category)
        return dict(categories_count=categories[0],
                    categories=categories[1],
                    mount_point=self.mount_point,
                    )

    @expose('tgappcategories.templates.new_category')
    def new_category(self, **_):
        return dict(form=get_new_category_form(),
                    mount_point=self.mount_point,
                    action=plug_url('tgappcategories', '/create_category'),
                    values=None,
                    )

    @expose()
    @validate(get_new_category_form(), error_handler=new_category)
    def create_category(self, **kwargs):
        dictionary = {
            'name': kwargs.get('name'),
            'description': kwargs.get('description'),
        }
        model.provider.create(model.Category, dictionary)

        flash(_('Category created.'))
        return redirect(url(self.mount_point))

    @expose('tgappcategories.templates.edit_category')
    def edit_category(self, category_id, **_):
        __, categories = model.provider.query(model.Category,
                                              filters={'_id': category_id})
        category = categories[0]
        return dict(form=get_edit_category_form(),
                    mount_point=self.mount_point,
                    action=plug_url('tgappcategories', '/update_category/' + category_id),
                    values=category,
                    )

    @expose()
    @validate(get_edit_category_form(), error_handler=edit_category)
    def update_category(self, category_id, **kwargs):
        __, categories = model.provider.query(model.Category,
                                              filters={'_id': category_id})
        category = categories[0]
        category.name = kwargs.get('name')
        category.description = kwargs.get('description')
        flash(_('Category updated.'))
        return redirect(url(self.mount_point))

    @expose()
    def delete_category(self, category_id):
        model.provider.delete(model.Category, dict(_id=category_id))
        flash(_('Category deleted'))
        return redirect(url(self.mount_point))
