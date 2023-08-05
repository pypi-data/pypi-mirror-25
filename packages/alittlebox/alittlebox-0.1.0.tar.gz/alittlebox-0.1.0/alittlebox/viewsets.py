from rest_framework import viewsets

class QuerysetModelViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return self.__class__.serializer_class.Meta.model.objects.all()
