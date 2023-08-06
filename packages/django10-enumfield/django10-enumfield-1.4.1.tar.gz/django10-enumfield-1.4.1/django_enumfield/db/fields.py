import django
from django.db import models
from django import forms
from django.utils import six

from django_enumfield import validators


if django.VERSION < (1, 8):
    base_class = six.with_metaclass(models.SubfieldBase, models.IntegerField)
else:
    base_class = models.IntegerField


class EnumField(base_class):
    """ EnumField is a convenience field to automatically handle validation of transitions
        between Enum values and set field choices from the enum.
        EnumField(MyEnum, default=MyEnum.INITIAL)
    """

    def __init__(self, enum, *args, **kwargs):
        kwargs['choices'] = enum.choices()
        if 'default' not in kwargs:
            kwargs['default'] = enum.default()
        self.enum = enum
        models.IntegerField.__init__(self, *args, **kwargs)

    def get_db_prep_value(self, value, connection, prepared=False):
        """Returns field's value prepared for interacting with the database
        backend.

        Used by the default implementations of get_db_prep_save().
        """
        validators.validate_available_choice(self.enum, value)
        return super(EnumField, self).get_db_prep_value(value, connection, prepared)

    def formfield(self, **kwargs):
        defaults = {'widget': forms.Select,
                    'form_class': forms.TypedChoiceField,
                    'coerce': int,
                    'choices': self.enum.choices(blank=self.blank)}
        defaults.update(kwargs)
        return super(EnumField, self).formfield(**defaults)

    def south_field_triple(self):
        """Returns a suitable description of this field for South."""
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector

        field_class = "django.db.models.fields.IntegerField"
        args, kwargs = introspector(self)
        # That's our definition!
        return field_class, args, kwargs

    def deconstruct(self):
        name, path, args, kwargs = super(EnumField, self).deconstruct()
        if django.VERSION >= (1, 9):
            kwargs['enum'] = self.enum
        else:
            path = "django.db.models.fields.IntegerField"
        if 'choices' in kwargs:
            del kwargs['choices']
        return name, path, args, kwargs
