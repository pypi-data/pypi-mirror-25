from tg.i18n import lazy_ugettext as l_
from tw2.core import Required
from tw2.forms.widgets import Form, TextField, TextArea, SubmitButton
from axf.bootstrap import BootstrapFormLayout


class KajikiBootstrapFormLayout(BootstrapFormLayout):
    inline_engine_name = 'kajiki'


class NewCategory(Form):    
    class child(KajikiBootstrapFormLayout):
        name = TextField(label=l_('Name'), css_class='form-control',
                         validator=Required)

        description = TextArea(label=l_('Description'), rows=10, css_class='form-control',
                               validator=Required)

    submit = SubmitButton(css_class='btn btn-primary pull-right', value=l_('Create'))


class EditCategory(NewCategory):
    submit = SubmitButton(css_class='btn btn-primary pull-right', value=l_('Edit'))
