import importlib

from rest_framework.fields import empty
from rest_framework import serializers

class StrMethodModelSerializer(serializers.ModelSerializer):
    """
    Appends a Model class' __str__ method to the serialized fields.
    """
    def get_default_field_names(self, declared_fields, model_info):
        return super(StrMethodModelSerializer, self).get_default_field_names(
            declared_fields, model_info
        ) + ['__str__', ]

class RelationalFieldsModelSerializer(StrMethodModelSerializer):
    """
    Appends all toOne as ?
    and toMany as HyperlinkedModelSerializer
    """
    def __init__(self, instance=None, data=empty, **kwargs):
        for f in self.Meta.model._meta.get_fields():
            # to One case
            if f.__class__.__name__ == 'ForeignKey':
                # create a field nesting the object the FK references
                setattr(
                    # serializer's instance
                    self,
                    # serializer's field name matching the model's
                    getattr(f, 'name'),
                    # dynamically constract the module and class
                    # of the appropriate serializer
                    getattr(
                        importlib.import_module(
                            f.model.__module__.replace('models', 'serializers')
                        ),
                        f.model.__name__ + 'Serializer'
                    )#(many=False, read_only=True)
                )
            # to Many cases
            elif f.__class__.__name__ in ['ManyToOneRel', 'ManyToManyRel', ]:
                # add a HyperlinkedModelSerializer field
                # to the referenced model's objects
                setattr(
                    # serializer's instance
                    self,
                    # serializer's field name matching the model's
                    getattr(f, 'name'),
                    serializers.HyperlinkedModelSerializer(
                        many=True, read_only=True,
                        # standard URL pattern name for simple routers
                        view_name = getattr(f, 'name') + '-detail'
                    )
                )
            # no else, we only care about relational fields
        super(RelationalFieldsModelSerializer, self).__init__(**kwargs)
