import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from adminsortable.models import Sortable
from adminsortable.fields import SortableForeignKey
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import Group
from cms.models import CMSPlugin


class DataCollection(models.Model):
    """
    Represents a data collection.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Title'), max_length=255)
    unique_titles = models.BooleanField(
        _('Unique titles'), default=False, blank=True,
        help_text=_('If checked than Title field for the records must be unique.'),
    )

    title_field_label = models.CharField(_('Title field label'), max_length=255, blank=True)
    active_field_label = models.CharField(_('Active field label'), max_length=255, blank=True)
    reversed_ordering = models.BooleanField(_('Reversed ordering'), default=False)

    added = models.DateTimeField(_('Added'), auto_now_add=True)
    changed = models.DateTimeField(_('Changed'), auto_now=True)

    class Meta:
        verbose_name = _('Data collection')
        verbose_name_plural = _('Data collections')
        ordering = ['title']

    def __str__(self) -> str:
        return self.title

    def get_records(self):
        if self.reversed_ordering:
            return self.records.order_by('-added', 'id')
        else:
            return self.records.all()


class DataCollectionFieldManager(models.Manager):
    def admin_list_display(self):
        return self.get_queryset().filter(admin_list_display=True)


class DataCollectionField(Sortable):
    """
    Represents a field for data collection scheme.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_collection = SortableForeignKey(
        DataCollection, verbose_name=_('Data collection'),
        related_name='fields')
    name = models.CharField(
        _('Name'), max_length=255,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z\-_][0-9a-zA-Z\-_]*$',
            message=_("Value may only contain the letters a-z, A-Z, digits, "
                      "minus and underscores, and can't start with a digit."))])
    title = models.CharField(_('Title'), max_length=255)

    # Field types
    STRING = "string"
    EMAIL = "email"
    TEXT = "text"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    CHOICE = "choice"
    MULTIPLE_CHOICE = "multiple_choice"
    FILE = "file"
    WYSIWYG = "wysiwyg"
    CODE = "code"
    DATE = "date"
    FIELD_TYPE_CHOICES = (
        (STRING, _("String")),
        (EMAIL, _("Email")),
        (TEXT, _("Multiline text")),
        (INTEGER, _("Integer")),
        (BOOLEAN, _("True / False")),
        (FLOAT, _("Float")),
        (CHOICE, _("Choice")),
        (MULTIPLE_CHOICE, _("Multiple choice")),
        (FILE, _("File")),
        (WYSIWYG, _("WYSIWYG")),
        (CODE, _("Code")),
        (DATE, _("Date")),
    )
    field_type = models.CharField(
        _('Field type'), max_length=20,
        default="string", choices=FIELD_TYPE_CHOICES)
    choices = models.TextField(
        _('Choices'), blank=True, default='',
        help_text=_(
            'Usable for Choice type. Type choices in different lines.'))
    help_text = models.TextField(_('Help text'), blank=True, default='')
    required = models.BooleanField(_('Required'), default=False, blank=True)

    admin_list_display = models.BooleanField(
        _('Admin list display'), default=False, blank=True)

    collection_order = models.PositiveIntegerField(
        default=0, editable=False, db_index=True)

    added = models.DateTimeField(_('Added'), auto_now_add=True)
    changed = models.DateTimeField(_('Changed'), auto_now=True)

    objects = DataCollectionFieldManager()

    class Meta:
        unique_together = ['data_collection', 'name']
        ordering = ['collection_order']
        verbose_name = _('Data collection field')
        verbose_name_plural = _('Data collection fields')

    def __str__(self) -> str:
        return self.title


# Rename fields if required
@receiver(pre_save, sender=DataCollectionField)
def rename_fields_at_records(sender, **kwargs):
    _field = kwargs['instance']
    if _field.id:
        try:
            _old_field = DataCollectionField.objects.get(pk=_field.id)
            if _field.name != _old_field.name:
                # Here we should rename fields for all records
                data_collection = _field.data_collection
                records = data_collection.records.all()
                for r in records.iterator():
                    _data = r.data
                    if _old_field.name in _data:
                        _data[_field.name] = _data[_old_field.name]
                        del _data[_old_field.name]
                        r.data = _data
                        r.save()
        except DataCollectionField.DoesNotExist:
            # Does it is a fixture loading?
            pass


class DataRecord(models.Model):
    """
    Represents a data collection record.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_collection = models.ForeignKey(
        DataCollection,
        verbose_name=_('Data collection'),
        related_name='records')
    title = models.CharField(_('Title'), max_length=255, blank=True)
    active = models.BooleanField(_('Active'), default=True, blank=True)

    data = JSONField(_('Data'), default=dict(), blank=True)

    added = models.DateTimeField(_('Added'), auto_now_add=True)
    changed = models.DateTimeField(_('Last change'), auto_now=True)

    class Meta:
        verbose_name = _('Data record')
        verbose_name_plural = _('Data records')
        ordering = ['added', 'id']

    def __str__(self) -> str:
        return self.title

    def as_dict(self):
        d = {
            'id': self.id,
            'title': self.title,
            'active': self.active,
        }
        d.update(self.data)
        return d


# Work with custom hooks
@receiver(post_save, sender=DataRecord)
def call_mail_hooks(sender, **kwargs):
    _record = kwargs['instance']
    _is_raw = kwargs['raw']
    if _is_raw:
        # Fixture loading
        return None
    data_collection = _record.data_collection
    if kwargs['created']:
        # New record
        mail_hooks = MailHook.objects.filter(
            data_collection=data_collection,
            active=True,
            event_type='new',
        )
        for hook in mail_hooks:
            hook.do_hook_for(_record)
    else:
        # Available record
        mail_hooks = MailHook.objects.filter(
            data_collection=data_collection,
            active=True,
            event_type='changed',
        )
        for hook in mail_hooks:
            hook.do_hook_for(_record)


class WebForm(models.Model):
    """
    Represents a custom web form based on a data collection.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Title'), max_length=255, unique=True)
    data_collection = models.ForeignKey(
        DataCollection,
        verbose_name=_('Data collection'),
        related_name='web_forms')
    fields = models.CharField(
        _('Fields'), max_length=255,
        default='',
        blank=True,
        help_text=_('Comma separated list of field names.'))
    hidden_fields = models.CharField(
        _('Hidden fields'), max_length=255,
        default='',
        blank=True,
        help_text=_(
            'Comma separated list of hidden fields. '
            'Must be subset of the "Fields" list.'))
    show_captcha = models.BooleanField(_('Show captcha'), default=False, blank=True)

    added = models.DateTimeField(_('Added'), auto_now_add=True)
    changed = models.DateTimeField(_('Last change'), auto_now=True)

    class Meta:
        verbose_name = _('Web form')
        verbose_name_plural = _('Web forms')
        ordering = ['title']

    def __str__(self) -> str:
        return self.title


class MailHook(models.Model):
    """
    Represents a mail hook.
    """
    EVENT_CHOICES = (
        ('new', _('New record')),
        ('changed', _('Changed')),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Title'), max_length=255, unique=True)
    active = models.BooleanField(_('Active'), default=True, blank=True)

    data_collection = models.ForeignKey(
        DataCollection,
        verbose_name=_('Data collection'),
        related_name='mail_hooks')
    event_type = models.CharField(
        _('Event type'),
        max_length=25,
        default='new',
        choices=EVENT_CHOICES,
    )
    user_group = models.ForeignKey(
        Group,
        verbose_name=_('User group'),
        null=True, blank=True,
        related_name='mail_hooks',
    )
    additional_emails = models.TextField(
        _('Additional emails'), blank=True, default='',
        help_text=_('Type the emails in different lines.'))

    email_template = models.ForeignKey(
        'pcart_messaging.EmailTemplate', verbose_name=_('Email template'),
        related_name='mail_hooks',
    )
    from_email = models.CharField(
        _('From email'),
        max_length=255,
        default=settings.DEFAULT_FROM_EMAIL,
        help_text=_(
            'You can use {{field_name}} for insert data from data record.')
    )

    added = models.DateTimeField(_('Added'), auto_now_add=True)
    changed = models.DateTimeField(_('Last change'), auto_now=True)

    class Meta:
        verbose_name = _('Mail hook')
        verbose_name_plural = _('Mail hooks')
        ordering = ['title']

    def __str__(self) -> str:
        return self.title

    def _render_text(self, text, context=None):
        from django.template import Context, Template
        _context = Context(context or {})
        template = Template(text)
        return template.render(_context)

    def do_hook_for(self, data_record, extra_context=None):
        from pcart_messaging.utils import send_email_to_group
        _data = data_record.as_dict()

        if self.user_group:
            _group_name = self.user_group.name
        else:
            _group_name = None

        context = {
            'data_record': data_record,
            'data_collection': data_record.data_collection,
            'hook': self,
        }
        context.update(_data)
        if extra_context is not None:
            context.update(extra_context)
        _additional_emails = []
        for e in self.additional_emails.splitlines():
            t = self._render_text(e, context)
            if t:
                _additional_emails.append(t)

        _from_email = self._render_text(
            self.from_email,
            context,
        )

        send_email_to_group(
            template_name=self.email_template.name,
            group_name=_group_name or 'mailhook',
            sender=_from_email,
            context=context,
            extra_recipients=_additional_emails,
        )


# CMS plugins

class WebFormPluginModel(CMSPlugin):
    """
    Represents a plugin with a web form.
    """
    web_form = models.ForeignKey(WebForm, verbose_name=_('Web form'))
    show_title = models.BooleanField(_('Show title'), default=True)
    title = models.CharField(
        _('Title'), max_length=255, default='', blank=True,
        help_text=_('Optional. If not set the web form title will be used.')
    )
    template_name = models.CharField(_('Template name'), default='default', blank=True, max_length=100)

    def __init__(self, *args, **kwargs):
        super(WebFormPluginModel, self).__init__(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.web_form)

