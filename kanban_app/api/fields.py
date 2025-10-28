from rest_framework import serializers
from rest_framework.exceptions import NotFound

class BoardPrimaryKeyField(serializers.PrimaryKeyRelatedField):
    """
    Extended PK field that returns 404 if the object doesn’t exist,
    instead of a ValidationError (400).
    """
    def get_queryset(self):
        if self.queryset is None:
            raise AssertionError(f'{self.__class__.__name__} muss ein queryset haben.')
        return self.queryset

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            return queryset.get(pk=data)
        except queryset.model.DoesNotExist:
            raise NotFound('Board nicht gefunden. Die angegebene Board-ID existiert nicht.')
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)