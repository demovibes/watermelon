from django.views.generic.list import ListView

from .models import Entry

# list view showing playlist
class EntryListView(ListView):
    model = Entry
    paginate_by = 100  # if pagination is desired

