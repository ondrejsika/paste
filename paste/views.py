import time

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from .models import Paste
from .forms import PasteForm


ALLOW_ANONYMOUS_PASTES = getattr(settings, 'ALLOW_ANONYMOUS_PASTES', False)


def index_view(request, template="paste/index.html"):
    pastes = Paste.objects.active()

    return render_to_response(template,
        {
            "title": "All pastes",

            "pastes": pastes,
        },
        context_instance=RequestContext(request))

@login_required
def index_my_view(request, template="paste/index.html"):
    pastes = Paste.objects.active().filter(owner=request.user.profile)

    return render_to_response(template,
        {
            "title": "My pastes",

            "pastes": pastes,
        },
        context_instance=RequestContext(request))

def add_view(request, template="paste/add.html"):
    add_paste_form = PasteForm(request.POST or None)
    if not request.user.is_authenticated():
        if not ALLOW_ANONYMOUS_PASTES:
            return HttpResponseForbidden("403 Forbidden")
        del add_paste_form.fields["private"]
    if add_paste_form.is_valid():
        paste = add_paste_form.save(commit=False)
        if request.user.is_authenticated():
            paste.owner = request.user.profile
        paste.save()
        return HttpResponseRedirect(reverse("paste:detail", args=(paste.pk, )))

    return render_to_response(template,
        {
            "title": "Add paste",

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
            "title": "%s / edit" % paste,
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
            "title": paste,
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
        "title": "%s / delete" % paste,
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

@login_required
def settings_view(request, template="paste/settings.html"):
    return render_to_response(template,
        {
            "title": "Settings",
        },
        context_instance=RequestContext(request))

@login_required
def change_password_view(request, template="paste/change_password.html"):
    change_password_form = PasswordChangeForm(data=request.POST or None, user=request.user)
    if change_password_form.is_valid():
        change_password_form.save()
        return HttpResponseRedirect(reverse("paste:change_password_done"))
    return render_to_response(template,
        {
            "change_password_form": change_password_form,
        },
        context_instance=RequestContext(request))
