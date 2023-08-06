from django.contrib.gis import admin
from django.utils.translation import ugettext_lazy as _
from adminsortable.admin import SortableStackedInline, NonSortableParentAdmin
from .models import (
    DataCollection,
    DataCollectionField,
    DataRecord,
    WebForm,
    MailHook,
)
from .forms import DataCollectionFieldAdminForm


class DataCollectionFieldInline(SortableStackedInline):
    model = DataCollectionField
    form = DataCollectionFieldAdminForm
    fieldsets = (
        (None, {
            'fields': ['name', 'title', 'field_type', 'required'],
        }),
        (_('Extra'), {
            'fields': ['choices', 'help_text', 'admin_list_display'],
            'classes': ('collapse',),
        }),
    )
    extra = 1


class DataCollectionAdmin(NonSortableParentAdmin):
    list_display = ['title', 'get_records_count', 'records_manage_link']
    inlines = [DataCollectionFieldInline]

    def get_records_count(self, obj):
        return obj.records.count()
    get_records_count.short_description = _('Records count')

    def records_manage_link(self, obj):
        from django.core.urlresolvers import reverse
        return '<a class="button" href="%s">%s</a>' % (
            reverse(
                'admin:datacollection_records_list',
                args=[obj.pk]),
            _('Data Records'),
        )
    records_manage_link.short_description = _('Actions')
    records_manage_link.allow_tags = True

    def records_list_view(self, request, collection_id):
        from django.shortcuts import render, get_object_or_404
        data_collection = get_object_or_404(
            DataCollection, id=collection_id)
        data_records = data_collection.get_records()

        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           data_collection=data_collection,
           data_records=data_records,
        )
        return render(
            request,
            'admin/data_collections/datacollection/datarecords_list.html',
            context)

    def record_change_view(self, request, collection_id, record_id=None):
        from django.shortcuts import render, redirect, get_object_or_404
        from django.core.urlresolvers import reverse
        from .forms import DataRecordForm

        data_collection = get_object_or_404(
            DataCollection, id=collection_id)

        data_record = None
        if record_id:
            data_record = get_object_or_404(
                DataRecord,
                data_collection=data_collection,
                id=record_id)

        if request.method == 'POST':
            if record_id:
                form = DataRecordForm(
                    request.POST,
                    request.FILES,
                    instance=data_record,
                    data_collection=data_collection,
                    request=request,
                )
            else:
                form = DataRecordForm(
                    request.POST,
                    request.FILES,
                    data_collection=data_collection,
                    request=request,
                )
            if form.is_valid():
                data_record = form.save()

                if '_save' in request.POST:
                    return redirect(
                        reverse(
                            'admin:datacollection_records_list',
                            args=[data_collection.pk]))
                elif '_addanother' in request.POST:
                    return redirect(
                        reverse(
                            'admin:datacollection_records_add',
                            args=[data_collection.pk]))
                elif '_continue' in request.POST:
                    return redirect(
                        reverse(
                            'admin:datacollection_records_change',
                            args=[data_collection.pk, data_record.pk]))
        else:
            if record_id:
                form = DataRecordForm(
                    instance=data_record,
                    data_collection=data_collection,
                    request=request,
                )
            else:
                form = DataRecordForm(
                    data_collection=data_collection,
                    request=request,
                )

        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           data_collection=data_collection,
           has_file_field=form.is_multipart(),
           show_save_and_add_another=True,
           show_save_and_continue=True,
           show_delete_link=False,
           form=form,
        )
        if record_id:
            context.update({
                'data_record': data_record,
                'show_delete_link': True,
            })
        return render(
            request,
            'admin/data_collections/datacollection/datarecord_change.html',
            context)

    def record_delete_view(self, request, collection_id, record_id):
        from django.shortcuts import redirect, get_object_or_404
        from django.core.files.storage import default_storage
        from django.core.urlresolvers import reverse

        data_collection = get_object_or_404(
            DataCollection, id=collection_id)
        collection_fields = DataCollectionField.objects.filter(
            data_collection=data_collection,
        ).order_by('collection_order')
        data_record = get_object_or_404(
            DataRecord,
            data_collection=data_collection,
            id=record_id)

        file_field_names = [
            f.name for f in collection_fields
            if f.field_type == DataCollectionField.FILE]
        for fn in file_field_names:
            _path = data_record.data.get(fn)
            if _path:
                default_storage.delete(_path)

        data_record.delete()
        return redirect(
            reverse(
                'admin:datacollection_records_list',
                args=[data_collection.pk]))

    def export_to_csv_view(self, request, collection_id):
        import csv
        from django.shortcuts import get_object_or_404
        from django.http import HttpResponse

        data_collection = get_object_or_404(
            DataCollection, id=collection_id)
        collection_fields = DataCollectionField.objects.filter(
            data_collection=data_collection,
        ).order_by('collection_order')

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename="%s.csv"' % data_collection.title

        writer = csv.writer(response)
        field_names = ['id', 'title', 'active']
        field_names += collection_fields.values_list('name', flat=True)
        writer.writerow(field_names)
        records = data_collection.records.all()

        for record in records:
            data = record.as_dict()
            line = [data.get(i) for i in field_names]
            writer.writerow(line)
        return response

    def import_from_csv_view(self, request, collection_id):
        from django.shortcuts import render, get_object_or_404
        from .forms import DataRecordImportForm, DataRecordForm
        import csv
        data_collection = get_object_or_404(
            DataCollection, id=collection_id)
        collection_fields = DataCollectionField.objects.filter(
            data_collection=data_collection,
        ).order_by('collection_order')

        report = []
        if request.method == 'POST':
            form = DataRecordImportForm(request.POST, request.FILES)
            if form.is_valid():
                # Import data
                _file = request.FILES['source']
                _content = b''
                for chunk in _file.chunks():
                    _content += chunk
                _content = _content.decode('utf-8')
                reader = csv.reader(_content.splitlines())
                i = 0
                headers = []
                for row in reader:
                    i += 1
                    status = ''
                    if i == 1:
                        # First line
                        headers = row
                    else:
                        # Line with data
                        _dict = dict(zip(headers, row))
                        for field in collection_fields:
                            if field.field_type == 'multiple_choice' and \
                                    field.name in _dict.keys():
                                if _dict[field.name] != '':
                                    _dict[field.name] = eval(_dict[field.name])

                        f = DataRecordForm(
                            _dict,
                            data_collection=data_collection,
                            request=request)
                        if f.is_valid():
                            # Data is valid
                            if 'id' in _dict and _dict['id'] != '':
                                id = _dict['id']
                                try:
                                    record = DataRecord.objects.get(
                                        id=id,
                                        data_collection=data_collection)
                                    f.instance = record
                                    record = f.save()
                                    status = 'CHANGED'
                                except DataRecord.DoesNotExist:
                                    record = f.save(commit=False)
                                    record.id = id
                                    record.save()
                                    status = 'CREATED'
                            else:
                                # id not specified
                                record = f.save()
                                status = 'CREATED'
                        else:
                            status = f.errors
                    report.append([status]+row)
        else:
            form = DataRecordImportForm()

        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           data_collection=data_collection,
           page_title=_('Import from CSV'),
           form=form,
           report=report,
        )
        return render(
            request,
            'admin/data_collections/datacollection/datarecords_import.html',
            context)

    def get_urls(self):
        from django.conf.urls import url
        urls = super().get_urls()
        list_urls = [
            url(
                r'^(?P<collection_id>[\w\d-]+)/datarecords/$',
                self.admin_site.admin_view(self.records_list_view),
                name='datacollection_records_list'),
            url(
                r'^(?P<collection_id>[\w\d-]+)/datarecords/add/$',
                self.admin_site.admin_view(self.record_change_view),
                name='datacollection_records_add'),
            url(
                r'^(?P<collection_id>[\w\d-]+)/datarecords/export-csv/$',
                self.admin_site.admin_view(self.export_to_csv_view),
                name='datacollection_export_to_csv_view'),
            url(
                r'^(?P<collection_id>[\w\d-]+)/datarecords/import-csv/$',
                self.admin_site.admin_view(self.import_from_csv_view),
                name='datacollection_import_from_csv_view'),
            url(
                r'^(?P<collection_id>[\w\d-]+)/datarecords/'
                r'(?P<record_id>[-\w\d]+)/change/$',
                self.admin_site.admin_view(self.record_change_view),
                name='datacollection_records_change'),
            url(
                r'^(?P<collection_id>[\w\d-]+)/datarecords/'
                r'(?P<record_id>[-\w\d]+)/delete/$',
                self.admin_site.admin_view(self.record_delete_view),
                name='datacollection_records_delete'),
        ]
        return list_urls + urls


admin.site.register(DataCollection, DataCollectionAdmin)


# class DataRecordAdmin(admin.ModelAdmin):
#     list_display = ['name', 'data_collection', 'active']
#     list_filter = ['data_collection']
#     search_fields = ['name']
#
# admin.site.register(DataRecord, DataRecordAdmin)


class WebFormAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'data_collection', 'fields', 'hidden_fields', 'show_captcha']
    list_filter = ['data_collection']
    search_fields = ['title']


admin.site.register(WebForm, WebFormAdmin)


class MailHookAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'active', 'data_collection', 'event_type', 'email_template', 'user_group']
    list_filter = ['data_collection']
    search_fields = ['title']
    fieldsets = (
        (None, {
            'fields': [
                'title', 'active', 'data_collection', 'event_type'],
        }),
        (_('Send to'), {
            'fields': ['user_group', 'additional_emails'],
        }),
        (_('Send from'), {
            'fields': ['from_email'],
        }),
        (_('Template'), {
            'fields': [
                'email_template',
            ],
        }),
    )


admin.site.register(MailHook, MailHookAdmin)
