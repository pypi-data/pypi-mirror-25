import tg
from tgext.pluggable import app_model
from .base import configure_app, create_app, flush_db_changes
from tgappcategories import model
import re
from webtest import AppError
find_urls = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


class RegistrationControllerTests(object):
    def setup(self):
        self.app = create_app(self.app_config, False)

    def test_index(self):
        resp = self.app.get('/')
        assert 'HELLO' in resp.text

    def test_tgappcategories_index(self):
        resp = self.app.get('/tgappcategories', extra_environ={'REMOTE_USER': 'manager'})

        assert '/new_category' in resp.text, resp

    def test_tgappcategories_auth(self):
        try:
            self.app.get('/tgappcategories')
        except AppError as e:
            assert '401' in str(e)

    def test_create_category(self):
        self.app.get('/tgappcategories/create_category',
                     params={'name': 'category one', 'description': 'pretty description'},
                     extra_environ={'REMOTE_USER': 'manager'},
                     status=302,
                     )
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category one'),
                                        )

        assert 'category one' == cats[0].name, cats[0].name
        assert 'pretty description' == cats[0].description, cats[0].description

    def test_update_category(self):
        self.app.get('/tgappcategories/create_category',
                     params={'name': 'category one', 'description': 'pretty description'},
                     extra_environ={'REMOTE_USER': 'manager'},
                     status=302,
                     )
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category one'),
                                        )

        self.app.get('/tgappcategories/update_category/' + str(cats[0]._id),
                     params={'name': 'edited category', 'description': 'edited description'},
                     extra_environ={'REMOTE_USER': 'manager'},
                     status=302,
                     )
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='edited category'),
                                        )

        assert 'edited category' == cats[0].name, cats[0].name
        assert 'edited description' == cats[0].description, cats[0].description

    def test_delete_category(self):
        self.app.get('/tgappcategories/create_category',
                     params={'name': 'category one', 'description': 'pretty description'},
                     extra_environ={'REMOTE_USER': 'manager'},
                     status=302,
                     )
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category one'),
                                        )

        self.app.get('/tgappcategories/delete_category/' + str(cats[0]._id),
                     extra_environ={'REMOTE_USER': 'manager'},
                     status=302,
                     )

        count, cats = model.provider.query(model.Category,
                                           filters=dict(name='category one'),
                                           )
        assert count == 0, cats

    def test_new_category_form(self):
        resp = self.app.get('/tgappcategories/new_category', extra_environ={'REMOTE_USER': 'manager'})

        assert 'name="name"' in resp.text, resp
        assert 'name="description"' in resp.text, resp
        assert '/create_category' in resp.text, resp

    def test_edit_category_form(self):
        self.app.get('/tgappcategories/edit_category', extra_environ={'REMOTE_USER': 'manager'}, status=404)

    def test_edit_category_form(self):
        self.app.get('/tgappcategories/create_category',
                     params={'name': 'category one', 'description': 'pretty description'},
                     extra_environ={'REMOTE_USER': 'manager'},
                     status=302,
                     )
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category one'),
                                        )

        resp = self.app.get('/tgappcategories/edit_category/' + str(cats[0]._id),
                            extra_environ={'REMOTE_USER': 'manager'}
                            )

        assert 'name="name"' in resp.text, resp
        assert 'name="description"' in resp.text, resp
        assert '/update_category' in resp.text, resp


class TestRegistrationControllerSQLA(RegistrationControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('sqlalchemy')


class TestRegistrationControllerMing(RegistrationControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('ming')