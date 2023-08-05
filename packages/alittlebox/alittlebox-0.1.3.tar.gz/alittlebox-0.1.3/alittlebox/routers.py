import importlib
import inspect

from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import Model

from django_filters import filterset
from rest_framework import filters, routers, pagination, serializers, viewsets

from alittlebox import filtersets

class DryRouterMixin(object):
    app_label = None # string, required
    exclude_models = [] # model names to exclude from the router
    serializer_classes = (serializers.ModelSerializer, )
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filterset_classes = (filterset.FilterSet, )
    pagination_class = pagination.LimitOffsetPagination
    viewset_classes = (viewsets.ModelViewSet, )
    def generate_filter_fileds(self, model):
        ALL = ['in', 'isnull', 'search', 'regex', 'iregex', ]
        NUMERICAL = ['exact', 'gte', 'lte', 'lt', 'gt', 'range', ]
        LOGICAL = ['exact', ]
        TEXTUAL = [
            'exact', 'iexact', 'contains', 'icontains',
            'startswith', 'istartswith', 'endswith', 'iendswith',
        ]
        CALENDAR = ['year', 'month', 'day', 'week_day', ]
        TEMPORAL = ['hour', 'minute', 'second', ]
        filterset_fields = {}
        for field in model._meta.get_fields():
            field_class_name = field.__class__.__name__
            if field_class_name in (
                'AutoField', 'BigAutoField', 'BigIntegerField',
                'DecimalField', 'FloatField',
                'IntegerField', 'PositiveIntegerField',
                'PositiveSmallIntegerField', 'SmallIntegerField',
            ):
                filterset_fields[field.name] = ALL + NUMERICAL
            elif field_class_name in ('BooleanField', 'NullBooleanField'):
                filterset_fields[field.name] = ALL + LOGICAL
            elif field_class_name in (
                'CharField', 'EmailField', 'FilePathField', 'SlugField',
                'TextField', 'URLField', 'UUIDField'
            ):
                filterset_fields[field.name] = ALL + TEXTUAL
            elif field_class_name in ('DateField', ):
                filterset_fields[field.name] = ALL + CALENDAR
            elif field_class_name in ('DateTimeField', ):
                filterset_fields[field.name] = ALL + CALENDAR + TEMPORAL
            elif field_class_name in ('TimeField', ):
                filterset_fields[field.name] = ALL + TEMPORAL
            elif field_class_name in (
                'ForeignKey', 'ManyToOneRel', 'OneToOneField',
                'ManyToManyField', 'ManyToManyRel',
            ):
                # filterset_fields[field.name] = LOGICAL
                pass #TODO: Related fields, also in the viewset.search_fields!
            elif field_class_name in (
                'FileField', 'ImageField', 'VideoField',
            ):
                pass #TODO: files
            else:
                pass
                #TODO: weird fields
                # 'BinaryField', 'CommaSeparatedIntegerField',
                # 'DurationField', 'GenericIPAddressField',
                #TODO: postgres only
                #//docs.djangoproject.com/en/1.11/ref/contrib/postgres/fields/
        return filterset_fields
    def get_urls(self):
        # get the app from a properly set app_label
        if type(self.app_label) != type(''):
            raise ImproperlyConfigured(
                "You must set the app_label attribute "
                "before including the router's urls in the patterns."
            )
        app = importlib.import_module(self.app_label + '.models')
        # convert all excluded model name to lower-case
        self.exclude_models = [m.lower() for m in self.exclude_models]
        for name, model in inspect.getmembers(app):
            if ( # iterate only classes defined in the app
                inspect.isclass(model)
            ) and ( # iterate only classes of Model type in their hierarchy
                Model in inspect.getmro(model)
            ) and ( # ignore all models the user has excluded (ignoring case))
                name.lower() not in self.exclude_models
            ) and ( # exclude abstract models
                # unfortunately, we have to instantiate to check for abstract
                not model()._meta.abstract
            ):
                # dynamically define the serializer class
                Serializer = type(
                    name+'Serializer', # class name
                    self.serializer_classes, # class hierarchy
                    { # attributes, in this case the class Meta
                        'Meta': type(
                            'Meta',
                            (object, ),
                            {
                                'model': model,
                                'fields': '__all__'
                            }
                        )
                    }
                )
                # dynamically define the filter set class
                Filterset = type(
                    name+'Filterset', # class name
                    self.filterset_classes, # class hierarchy
                    { # attributes, in this case the class Meta
                        'Meta': type(
                            'Meta',
                            (object, ),
                            {
                                'model': model,
                                'fields': self.generate_filter_fileds(model),
                            }
                        )
                    }
                )
                # dynamically define the viewset class
                Viewset = type(
                    name+'Viewset', # class name
                    self.viewset_classes, # class hierarchy
                    { # attributes
                        'filter_backends': self.filter_backends,
                        'filter_class': Filterset,
                        'search_fields': [
                            f.name for f in model._meta.get_fields(
                                include_hidden=True
                            ) if f.__class__.__name__ not in [
                                'ForeignKey', 'ManyToManyField',
                                'ManyToManyRel',
                                'ManyToOneRel', 'OneToOneField',
                            ]
                        ],
                        'pagination_class': self.pagination_class,
                        'serializer_class': Serializer,
                    }
                )
                # finally register the viewset
                self.register(
                    name.lower(), # prefix
                    Viewset, # viewset class
                    name.lower() # base_name
                )
        return super(DryRouterMixin, self).get_urls()

class DryDefaultRouter(DryRouterMixin, routers.DefaultRouter):
    pass

class DrySimpleRouter(DryRouterMixin, routers.SimpleRouter):
    pass

def test(field):
    # print(field, field.__class__.__name__)
    return field
