from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import Form, ValidationError
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from .models import CollectionType, Collection, CollectionMeta


# #############################################################################
# List page of a Collection Type
class CollectionList(ListView):
    model = Collection

    def get_queryset(self):
        queryset = super().get_queryset()
        self.collection_type = get_object_or_404(CollectionType, id=self.kwargs["collection_type"])
        return queryset.filter(collection_type=self.collection_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collection_type'] = self.collection_type
        return context


# #############################################################################
# Specific page of an Collection
class CollectionDetail(DetailView):
    model = Collection

    # Do not display "inactive" collections to non-staff.
    def get_queryset(self):
        queryset = super().get_queryset()
        #self.collection_type = get_object_or_404(CollectionType, id=self.kwargs["collection_type"])
        #queryset = queryset.filter(collection_type=self.collection_type)
        if (self.request.user.is_staff):
            return queryset
        return queryset.filter(is_active=True)

# #############################################################################
# Admin index page for Collection Meta request
class CollectionMetaList(PermissionRequiredMixin, ListView):
    permission_required = 'collections.view_collectionmeta'
    model = CollectionMeta

    # Display only "active" metadata requests.
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(reviewed=False)

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        self.collection_type = get_object_or_404(CollectionType, name=self.kwargs["collection_type"])
#        context['collection_type'] = self.collection_type
#        return context

# #############################################################################
# Specific page of an Collection Meta
#  this is a "dual" view that responds differently by POST or GET
class CollectionMetaDual(View):

    def get(self, request, *args, **kwargs):
        view = CollectionMetaDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CollectionMetaForm.as_view()
        return view(request, *args, **kwargs)

class CollectionMetaDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'collections.view_collectionmeta'
    model = CollectionMeta

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

#        self.collection_type = get_object_or_404(CollectionType, name=self.kwargs["collection_type"])
#        context['collection_type'] = self.collection_type.name

        # fill in the table of "changed fields"
        context['changed_fields'] = []
        changed_field_names = self.object.changed_fields.split()

        for field in changed_field_names:
            context['changed_fields'].append( {
                'name': field,
                'current': getattr(self.object.collection, field),
                'new': getattr(self.object, field)
            } )

        # add a form for approve / reject
        context['form'] = Form()
        return context


# #############################################################################
class CollectionMetaForm(PermissionRequiredMixin, SingleObjectMixin, FormView):
    permission_required = 'collections.change_collectionmeta'
    template_name = 'collectionmeta_detail.html'
    form_class = Form
    model = CollectionMeta

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # switch behavior based on accept or reject
        if 'accept' in form.data:
            # copy all changed fields to the parent collection and save
            for field in self.object.changed_fields.split():
                field_type = self.object._meta.get_field(field)
                if (isinstance(field_type, ManyToManyField)):
                    getattr(self.object.collection, field).set(getattr(self.object, field).all())
                else:
                    setattr(self.object.collection, field, getattr(self.object, field))

            # save the parent collection
            self.object.collection.save()

            # set ourselves as approved
            self.object.accepted = True
        elif 'reject' in form.data:
            self.object.accepted = False
        else:
            raise ValidationError('Invalid POST request', code='invalid')

        # in either case, mark this as reviewed
        self.object.reviewed = True
        self.object.save()

        # carry on
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('collections:collectionmeta-list', kwargs={'collection_type': self.object.collection.collection_type.id})

# #############################################################################
# Render a form allowing collection metadata changes
class CollectionMetaCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'collections.create_collectionmeta'
    model = CollectionMeta

    fields = [ 'name', 'image', 'description', 'artists', 'songs', ]

    # the get and post must retrieve the COLLECTION base, not COLLECTION META.
    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super().get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        # lookup the base object using the provided pk from kwargs
        collection = Collection.objects.get(pk=self.kwargs['collection_id'])
        for field in self.fields:
            # copy all changed fields to the parent collection and save
            field_type = collection._meta.get_field(field)
            if (isinstance(field_type, ManyToManyField)):
                initial[field] = getattr(collection, field).all()
            else:
                initial[field] = getattr(collection, field)

        return initial

    def form_valid(self, form):
        # Get collection ID we are supposed to be editing
        collection_id = self.kwargs["collection_id"]

        # set this on the form so it has the value attached
        form.instance.collection_id = collection_id

        # set the submitter to be the current user
        form.instance.submitter = self.request.user

        # set the "changed fields" on this request too
        form.instance.changed_fields = " ".join(form.changed_data)

        # if user doesn't have permission to view the result, send them
        #  back to the Collection page instead
        if ( self.request.user.has_perm('collections.view_collectionmeta') == False ):
            self.success_url = reverse('collections:collection-detail', kwargs={'collection_type': self.kwargs["collection_type"], 'pk': collection_id})
        return super().form_valid(form)
