import json
from django.shortcuts import (
    redirect,
    render,
    get_object_or_404,
)
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseForbidden, HttpResponse
from django.conf import settings
from .models import DataCollection, DataRecord, WebForm
from .forms import DataRecordForm, DataRecordSiteForm


def show_web_form(request):
    """
    Returns a form code via AJAX with specified template.
    """
    if not request.is_ajax():
        return HttpResponseForbidden('AJAX request required.')

    # Check the form title
    form_title = request.GET.get('title')
    if form_title is None:
        return HttpResponseForbidden('You should set the "title" argument.')

    # Check the form template
    view = request.GET.get('view', 'default')
    template_name = settings.PCART_WEB_FORM_TEMPLATES.get(view)
    if template_name is None:
        return HttpResponseForbidden('You should specify the correct "view" argument value.')

    web_form = get_object_or_404(WebForm, title__exact=form_title)
    form = DataRecordSiteForm(
        request=request,
        web_form=web_form,
    )

    target_id = request.GET.get('target-id')
    context = {
        'web_form': web_form,
        'form': form,
        'view': view,
        'form_result': False,
        'target_id': '#%s' % target_id or '',
    }
    return render(request, template_name, context)


@require_POST
@csrf_exempt
def data_collection_default_action(request):
    from urllib.parse import urlencode
    http_host = request.META.get('HTTP_HOST')
    current_site = get_current_site(request).domain
    if http_host != current_site:
        return HttpResponseForbidden('Request does not allowed.')

    web_form = None
    data_collection = None
    if 'web-form' in request.POST:
        web_form = get_object_or_404(
            WebForm,
            title__exact=request.POST['web-form']
        )
        data_collection = web_form.data_collection
    else:
        return HttpResponseForbidden('"web-form" attribute is required')

    if 'record-id' in request.POST:
        instance = get_object_or_404(
            DataRecord,
            data_collection=data_collection,
            id=request.POST['record-id'],
        )
    else:
        instance = None

    if instance:
        form = DataRecordSiteForm(
            request.POST,
            request.FILES,
            instance=instance,
            web_form=web_form,
            request=request,
        )
    else:
        form = DataRecordSiteForm(
            request.POST,
            request.FILES,
            web_form=web_form,
            request=request,
        )

    # Check the form template
    view = request.POST.get('view', 'default')
    template_name = settings.PCART_WEB_FORM_TEMPLATES.get(view)
    if template_name is None:
        return HttpResponseForbidden('You should specify the correct "view" argument value.')

    valid = False
    form_result = False
    if form.is_valid():
        valid = True
        instance = form.save()
        form_result = True
    else:
        instance = None
        # _errors = form.errors
        # errors_dict = dict()
        # for e in _errors.keys():
        #     errors_dict.update({e: _errors[e]})
        # print(errors_dict)
        # _get_args = urlencode(errors_dict)
        # print(_get_args)

    target_id = request.POST.get('target-id')
    context = {
        'web_form': web_form,
        'form': form,
        'view': view,
        'instance': instance,
        'valid': valid,
        'form_result': form_result,
        'target_id': '#%s' % target_id or '',
    }
    return render(request, template_name, context)

