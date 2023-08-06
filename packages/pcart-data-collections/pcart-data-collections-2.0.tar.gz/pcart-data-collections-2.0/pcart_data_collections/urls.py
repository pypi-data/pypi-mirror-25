from django.conf.urls import url
from .views import (
    show_web_form,
    data_collection_default_action,
)

urlpatterns = [
    url(
        r'^webform-show/$',
        show_web_form,
        name='show_web_form'),
    url(
        r'^webform-default-action/$',
        data_collection_default_action,
        name='data_collection_default_action'),
]
