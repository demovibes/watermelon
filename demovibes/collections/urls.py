from django.urls import path

from django.views.generic.list import ListView

from .models import Collection, CollectionType
from .views import (CollectionList, CollectionDetail, CollectionMetaCreate, CollectionMetaDual, CollectionMetaList)

app_name = 'collections'

urlpatterns = [
    # Admin list and detail for collection metadata
    path('<slug:collection_type>/meta/<int:pk>/', CollectionMetaDual.as_view(), name='collectionmeta-detail'),
    path('<slug:collection_type>/meta/', CollectionMetaList.as_view(), name='collectionmeta-list'),

    # User to create new collection meta
    path('<slug:collection_type>/<int:collection_id>/edit/', CollectionMetaCreate.as_view(), name='collectionmeta-create'),

    # Public read access to collection info
    path('<slug:collection_type>/<int:pk>/', CollectionDetail.as_view(), name='collection-detail'),
    path('<slug:collection_type>/', CollectionList.as_view( model=Collection, paginate_by=100 ), name='collection-list'),

    # Collection types
    path('', ListView.as_view( model=CollectionType, paginate_by=100 ), name='collection-type-list'),
]
