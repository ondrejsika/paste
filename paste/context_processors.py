from django.conf import settings


ALLOW_ANONYMOUS_PASTES = getattr(settings, 'ALLOW_ANONYMOUS_PASTES', False)


def paste(request):
    return {
        'show_add_paste': request.user.is_authenticated() or ALLOW_ANONYMOUS_PASTES,
    }
