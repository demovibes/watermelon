from .forms import ChatForm
from .models import Message


def chat_recent(request):
    return {
        'messages': Message.objects.all()[:10],
    }
