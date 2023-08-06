from django.utils.translation import ugettext_lazy as _
from django.forms import (
    IntegerField,
    FloatField,
    ChoiceField,
    MultipleChoiceField,
    CharField,
    EmailField,
    BooleanField,
    FileField,
    DateField,
    HiddenInput,
    ValidationError,
    ModelForm,
    Form,
)
from django.forms.widgets import (
    TextInput,
    Textarea,
    ClearableFileInput,
)
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django_ace import AceWidget

from datetimewidget import widgets as datetime_widgets
from djangocms_text_ckeditor.widgets import TextEditorWidget
from captcha.fields import ReCaptchaField
from .models import DataCollectionField, DataRecord, WebFormPluginModel


class DataRecordImportForm(Form):
    source = FileField(label=_('File'), required=True)


class DataCollectionFieldAdminForm(ModelForm):
    class Meta:
        model = DataCollectionField
        fields = '__all__'
        widgets = {
            'help_text': TextInput(attrs={'class': 'vTextField'}),
        }


class DataRecordForm(ModelForm):

    class Meta:
        model = DataRecord
        fields = ['title', 'active']

    WIDGETS = {
        DataCollectionField.TEXT: Textarea,
        DataCollectionField.CODE: AceWidget(
            wordwrap=False,
            width="100%",
            height="300px",
            showprintmargin=True),
        DataCollectionField.FILE: ClearableFileInput,
        DataCollectionField.DATE: admin_widgets.AdminDateWidget,
    }
    FIELD_CLASSES = {
        DataCollectionField.TEXT: CharField,
        DataCollectionField.EMAIL: EmailField,
        DataCollectionField.WYSIWYG: CharField,
        DataCollectionField.CODE: CharField,
        DataCollectionField.STRING: CharField,
        DataCollectionField.INTEGER: IntegerField,
        DataCollectionField.FLOAT: FloatField,
        DataCollectionField.CHOICE: ChoiceField,
        DataCollectionField.MULTIPLE_CHOICE: MultipleChoiceField,
        DataCollectionField.FILE: FileField,
        DataCollectionField.BOOLEAN: BooleanField,
        DataCollectionField.DATE: DateField,
    }

    error_messages = {
        'title_is_not_unique': _('Title must be unique.'),
        'title_same_multiple_found':
        _('Fix your database. More than one same Title found.'),
    }

    def _get_field_widget(self, field):
        if field.field_type == DataCollectionField.CODE:
            if field.choices:
                _mode = field.choices.splitlines()[0]
            else:
                _mode = 'default'
            return self.WIDGETS.get(field.field_type)(mode=_mode)
        else:
            return self.WIDGETS.get(field.field_type)

    def _get_field_object(self, field):
        _field_class = self.FIELD_CLASSES.get(field.field_type)
        _widget = self._get_field_widget(field)
        _field_obj = _field_class(
            label=field.title,
            required=field.required,
            help_text=field.help_text,
            widget=_widget
        )

        if field.field_type == DataCollectionField.CHOICE:
            _choices = [(t, t) for t in field.choices.splitlines()]
            _choices = [('', '-----')] + _choices
            _field_obj.choices = _choices
        elif field.field_type == DataCollectionField.MULTIPLE_CHOICE:
            _choices = [(t, t) for t in field.choices.splitlines()]
            _field_obj.choices = _choices
        elif field.field_type == DataCollectionField.FILE:
            _field_obj.is_file_upload = True
        elif field.field_type == DataCollectionField.BOOLEAN:
            _field_obj.is_checkbox = True
        return _field_obj

    def clean_name(self):
        name = self.cleaned_data['name']
        if self.data_collection.unique_names:
            try:
                record = DataRecord.objects.get(
                    data_collection=self.data_collection,
                    name__exact=name,
                )
                if hasattr(self, 'instance'):
                    if self.instance.pk == record.pk:
                        # Trying to save available record
                        return name
                raise ValidationError(
                    self.error_messages['name_is_not_unique'])
            except DataRecord.DoesNotExist:
                return name
            except DataRecord.MultipleObjectsReturned:
                raise ValidationError(
                    self.error_messages['name_same_multiple_found'])
        else:
            return name

    def __init__(self, *args, **kwargs):
        from django.core.files.storage import default_storage

        class FakeField:
            storage = default_storage

        data_collection = kwargs.pop('data_collection')
        self.data_collection = data_collection
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        collection_fields = self.get_collection_fields()

        self.fields['active'].is_checkbox = True
        if data_collection.title_field_label:
            self.fields['title'].label = data_collection.title_field_label
        if data_collection.active_field_label:
            self.fields['active'].label = data_collection.active_field_label

        for field in collection_fields:
            _field_name = field.name
            self.fields[_field_name] = self._get_field_object(field)

            # Initialize fields if an instance is specified
            if 'instance' in kwargs:
                data_record = kwargs.get('instance')
                custom_data = data_record.data
                _initial = custom_data.get(_field_name)
                if _initial is not None:
                    self.fields[_field_name].initial = _initial
                    if field.field_type == DataCollectionField.FILE:
                        from django.db.models.fields.files import FieldFile
                        _ff = FieldFile(None, FakeField, _initial)
                        self.fields[_field_name].initial = _ff

            # Initialize fields via GET arguments
            if _field_name in self.request.GET:
                self.fields[_field_name].initial = self.request.GET.get(_field_name, '')

    def get_collection_fields(self):
        collection_fields = DataCollectionField.objects.filter(
            data_collection=self.data_collection,
        ).order_by('collection_order')
        return collection_fields

    def get_upload_path(self, data_record, field):
        import os
        from django.utils.text import slugify
        _base_upload_path = os.path.join(
            'data-collections',
            self.data_collection.name,
            slugify(data_record.name),
        )
        _upload_path = os.path.join(
            _base_upload_path,
            field.name,
        )
        return _upload_path

    def save(self, force_insert=False, force_update=False, commit=True):
        import os
        from django.core.files.storage import default_storage
        from django.core.files.base import File
        from django.utils.text import slugify

        data_record = super().save(commit=False)
        # Save record properly
        custom_data = {}

        if hasattr(self, 'instance'):
            record_id = self.instance.pk
        else:
            record_id = None

        collection_fields = self.get_collection_fields()

        for field in collection_fields:
            if field.field_type == DataCollectionField.FILE:
                if field.name in self.request.FILES:
                    _upload_path = self.get_upload_path(data_record, field)
                    _file = self.request.FILES[field.name]
                    _file_name = self.cleaned_data[field.name].name
                    _t = os.path.splitext(_file_name)
                    _file_name = '%s%s' % (slugify(_t[0]), _t[1])
                    _dest_name = os.path.join(
                        _upload_path,
                        _file_name)
                    _path = default_storage.save(
                        _dest_name, File(_file))
                    custom_data[field.name] = _path
                elif ('%s-clear' % field.name) in self.request.POST:
                    _path = data_record.data.get(field.name)
                    if _path:
                        default_storage.delete(_path)
                else:
                    if record_id:
                        if isinstance(data_record.data, dict):
                            _t = data_record.data.get(field.name)
                            # print(_t, str(self.cleaned_data[field.name]))
                            if _t not in ['None', None]:
                                custom_data[field.name] = _t
                            else:
                                # print(self.cleaned_data)
                                custom_data[field.name] = \
                                    str(self.cleaned_data[field.name])
                        else:
                            custom_data[field.name] = \
                                str(self.cleaned_data[field.name])
            elif field.field_type == DataCollectionField.DATE:
                custom_data[field.name] = str(self.cleaned_data[field.name])
                """
                Use something like that for query:
                DataRecord.objects.raw(
                    'select * from datacollections_datarecord where '
                    'to_date(data->>\'birthday\',\'YYYY-MM-DD\') '
                    'between \'1981-10-10\' and \'1981-12-12\'')
                """
            elif field.field_type == DataCollectionField.INTEGER:
                custom_data[field.name] = int(self.cleaned_data[field.name])
            elif field.field_type == DataCollectionField.FLOAT:
                custom_data[field.name] = float(self.cleaned_data[field.name])
            elif field.field_type == DataCollectionField.BOOLEAN:
                custom_data[field.name] = bool(self.cleaned_data[field.name])
            else:
                custom_data[field.name] = self.cleaned_data[field.name]
        data_record.data = custom_data
        data_record.data_collection = self.data_collection

        if commit:
            data_record.save()
        return data_record


class DataRecordSiteForm(DataRecordForm):

    WIDGETS = {
        DataCollectionField.TEXT: Textarea,
        DataCollectionField.WYSIWYG: TextEditorWidget,
        DataCollectionField.CODE: AceWidget(
            wordwrap=False,
            width="100%",
            height="300px",
            showprintmargin=True),
        DataCollectionField.FILE: ClearableFileInput,
        DataCollectionField.DATE: datetime_widgets.DateWidget(
            usel10n=True, bootstrap_version=3,
            options={'format': 'yyyy-mm-dd'}),
    }

    def __init__(self, *args, **kwargs):
        self.web_form = kwargs.pop('web_form')
        kwargs.update({
            'data_collection': self.web_form.data_collection
        })
        super().__init__(*args, **kwargs)

        # Remove standard fields if required
        field_list = self.web_form.fields.split(',')
        if 'active' not in field_list:
            del self.fields['active']
        if 'title' not in field_list:
            del self.fields['title']

        hidden_fields = self.web_form.hidden_fields.split(',')
        for f in hidden_fields:
            if f in field_list:
                self.fields[f].widget = HiddenInput()

        if self.web_form.show_captcha:
            self.fields['captcha'] = ReCaptchaField()

    def get_collection_fields(self):
        field_list = self.web_form.fields.split(',')

        collection_fields = super().get_collection_fields()
        return collection_fields.filter(name__in=field_list)


class WebFormPluginForm(ModelForm):
    model = WebFormPluginModel

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(WebFormPluginForm, self).__init__(*args, **kwargs)
        self.fields['template_name'] = ChoiceField(
            choices=settings.PCART_WEB_FORM_TEMPLATES.items(),
            label=_('Template name'),
        )
