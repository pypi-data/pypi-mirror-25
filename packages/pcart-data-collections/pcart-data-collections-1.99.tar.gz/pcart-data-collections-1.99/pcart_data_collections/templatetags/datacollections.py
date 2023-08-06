import re
from django import template
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.core.cache import cache
from ..models import (
    DataCollection,
    DataCollectionField,
    DataRecord,
)

register = template.Library()


@register.inclusion_tag('datacollections/_field_value.html')
def render_field_value_as_html(
        data_record, field, image_width=100, domain=''):
    if isinstance(field, DataCollectionField):
        field_obj = field
    else:
        field_obj = data_record.data_collection.fields.get(name=field)
    _data = data_record.as_dict()
    return {
        'data_record': data_record,
        'field_obj': field_obj,
        'value': _data.get(field_obj.name),
        'image_width': image_width,
        'domain': domain,
    }


@register.simple_tag()
def list_of_dicts(objects_items):
    return [i.as_dict() for i in objects_items]


@register.filter
def data_values(queryset):
    return queryset.values()


@register.filter
def values_of(sequence, argument):
    return [i.get(argument) for i in sequence]


@register.filter
def get_item(sequence, index):
    return sequence.get(index)


@register.filter
def file_name(fullpath):
    import os
    return os.path.split(fullpath)[-1]


@register.filter
def is_image(fullpath):
    import os
    ext = os.path.splitext(fullpath)[-1].lower()
    return ext in ['.png', '.gif', '.jpg', '.jpeg', '.svg']
