import importlib
import inspect

from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import Model

from rest_framework import routers, serializers, viewsets

class DryRouterMixin(object):
    app_label = None # string, required
    exclude_models = [] # model names to exclude from the router
    serializer_classes = (serializers.ModelSerializer, )
    #TODO: filter_backends = (
    #     filters.OrderingFilter,
    #     filters.SearchFilter, filters.DjangoFilterBackend,
    # )
    #TODO: pagination_classes = ()
    viewset_classes = (viewsets.ModelViewSet, )
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
                #TODO: dynamically define the filter set class
                #TODO: dynamically define the pagination class
                # dynamically define the viewset class
                Viewset = type(
                    name+'Viewset', # class name
                    self.viewset_classes, # class hierarchy
                    { # attributes
                        'serializer_class': Serializer,
                        #TODO: filter set class
                        #TODO: pagination class
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
