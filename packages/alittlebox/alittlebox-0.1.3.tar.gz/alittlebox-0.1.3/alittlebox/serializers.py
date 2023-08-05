import importlib

from rest_framework import serializers
from rest_framework import fields

class StrMethodModelSerializer(serializers.ModelSerializer):
    """
    Appends a Model class' __str__ method to the serialized fields.
    """
    def get_default_field_names(self, declared_fields, model_info):
        return super(StrMethodModelSerializer, self).get_default_field_names(
            declared_fields, model_info
        ) + ['__str__', ]

class RelationalFieldsModelSerializer(serializers.ModelSerializer):
    """
    Appends all to-One as nested seriliazed objects
    and to-Many as HyperlinkedModelSerializerField lists.
    This requires that all relations declare the related_name attribute.
    """
    def __init__(self, *args, **kwargs):
        for f in self.Meta.model._meta.get_fields():
            # to One cases
            if f.__class__.__name__ in [
                'ForeignKey', 'OneToOneField',
            ]:
                name = getattr(f, 'name')
                # create a field nesting the object the FK references
                self.fields.update(
                    {
                        name: type(
                            name[0].upper()+name[0:]+'Serializer', # classname
                            (StrMethodModelSerializer, ), # class hierarchy
                            { # attributes, in this case the class Meta
                                'Meta': type(
                                    'Meta',
                                    (object, ),
                                    {
                                        'model': f.related_model,
                                        'fields': '__all__'
                                    }
                                )
                            }
                        )(many=False, read_only=False)
                    }
                )
            # to Many cases
            elif f.__class__.__name__ in [
                'ManyToOneRel', 'ManyToManyRel',
            ]:
                # add a HyperlinkedModelSerializerField
                # of the field's referenced model's API detail view
                self.fields.update(
                    {
                        getattr(
                            f, 'related_name'
                        ): serializers.HyperlinkedRelatedField(
                            many=True, read_only=True,
                            # standard URL pattern name for simple routers
                            view_name = getattr(
                                f, 'related_model'
                            ).__name__.lower() + '-detail'
                        )
                    }
                )
            # no else, we only care about relational fields
        super(RelationalFieldsModelSerializer, self).__init__(*args, **kwargs)
