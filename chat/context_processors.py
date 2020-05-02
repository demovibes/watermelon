from .models import Message
from .forms import ChatForm

def chat_recent(request):
    return {
        'messages': Message.objects.all()[:10],
    }
