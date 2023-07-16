from .models import CollectionType


def collection_types(request):
    # Copies all Collection Types to a dict
    return {
        'collection_types': [ { 'id': ct.id, 'name': ct.name } for ct in CollectionType.objects.all() ]
    }
