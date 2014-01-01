import time

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required

from .models import Paste
from .forms import PasteForm


def index_view(request, template="paste/index.html"):
    pastes = Paste.objects.active()

    return render_to_response(template,
        {
            "pastes": pastes,
        },
        context_instance=RequestContext(request))

def add_view(request, template="paste/add.html"):
    add_paste_form = PasteForm(request.POST or None)
    if add_paste_form.is_valid():
        paste = add_paste_form.save(commit=False)
        if request.user:
            paste.owner = request.user.profile
        paste.save()
        return HttpResponseRedirect(reverse("paste:detail", args=(paste.pk, )))

    return render_to_response(template,
        {
            "add_paste_form": add_paste_form,
        },
        context_instance=RequestContext(request))

@login_required
def edit_view(request, paste_pk, template="paste/edit.html"):
    paste = get_object_or_404(Paste, pk=paste_pk)
    if paste.owner != request.user.profile:
        return HttpResponseForbidden("403 Forbidden")

    edit_paste_form = PasteForm(request.POST or None, instance=paste)
    if edit_paste_form.is_valid():
        edit_paste_form.save()
        return HttpResponseRedirect(reverse("paste:detail", args=(paste.pk, )))

    return render_to_response(template,
        {
            "paste": paste,

            "edit_paste_form": edit_paste_form,
        },
        context_instance=RequestContext(request))


def detail_view(request, paste_pk, template="paste/detail.html"):
    paste = get_object_or_404(Paste, pk=paste_pk, deleted=False)
    if paste.private:
        if not request.user.is_authenticated():
            return HttpResponseForbidden("403 Forbidden")
        elif paste.owner != request.user.profile:
            return HttpResponseForbidden("403 Forbidden")

    return render_to_response(template,
        {
            "paste": paste,
        },
        context_instance=RequestContext(request))

def raw_view(request, paste_pk):
    paste = get_object_or_404(Paste, pk=paste_pk, deleted=False)
    if paste.private:
        if not request.user.is_authenticated():
            return HttpResponseForbidden("403 Forbidden")
        elif paste.owner != request.user.profile:
            return HttpResponseForbidden("403 Forbidden")

    return HttpResponse(paste.content, content_type="text/plain")

@login_required
def delete_view(request, paste_pk, template="paste/delete.html"):
    paste = get_object_or_404(Paste, pk=paste_pk)
    if paste.owner != request.user.profile:
        return HttpResponseForbidden("403 Forbidden")

    return render_to_response(template,
    {
        "paste": paste,
    },
    context_instance=RequestContext(request))

@login_required
def delete_process(request, paste_pk):
    paste = get_object_or_404(Paste, pk=paste_pk)
    if paste.owner != request.user.profile:
        return HttpResponseForbidden("403 Forbidden")

    paste.deleted = True
    paste.save()
    return HttpResponseRedirect(request.GET.get("next", "/"))
