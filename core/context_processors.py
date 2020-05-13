from .models import Setting


def settings(request):
    # Copies all settings from the key/value store into a dict
    return {
        'settings': { s.key: s.value for s in Setting.objects.all() }
    }
