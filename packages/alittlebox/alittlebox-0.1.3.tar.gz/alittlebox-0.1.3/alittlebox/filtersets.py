class AllFieldsMixin(object):
    def get_fields(self, model):
        filterList = {}
        for field in model._meta.get_fields():
            fieldType = field.__class__.__name__
            if fieldType in ('PositiveSmallIntegerField', 'FloatField'):
                actions = ['exact', 'gte', 'lte', 'lt', 'gt',
                           'range', 'isnull', 'search', 'regex', 'iregex']
            elif fieldType in ('CharField', 'TextField', 'URLField', 'UUIDField'):
                actions = ['exact', 'iexact', 'contains', 'icontains', 'startswith',
                           'istartswith', 'endswith', 'iendswith', 'isnull',
                           'search', 'regex', 'iregex']
            elif fieldType in ('DateField'):
                actions = ['year', 'month', 'day',
                           'week_day', 'isnull', 'search', 'regex', 'iregex']
            elif fieldType in ('DateTimeField'):
                actions = ['year', 'month', 'day', 'week_day',
                           'hour', 'minute', 'second', 'isnull', 'search',
                           'regex', 'iregex']
            elif fieldType in ('BooleanField'):
                actions = ['exact', 'isnull', 'search', 'regex', 'iregex']
            else:
                # print(field, fieldType, 'defaulting to exact match only')
                actions = ['exact']
            filterList[field.name] = actions
        return filterList
