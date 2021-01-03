from .models import Message
from .views import MessagePost


def chat_recent(request):
    p = MessagePost(request = request)

    return {
        'chat_messages': Message.objects.all()[:10],
        'chat_form': p.get_form()
    }
