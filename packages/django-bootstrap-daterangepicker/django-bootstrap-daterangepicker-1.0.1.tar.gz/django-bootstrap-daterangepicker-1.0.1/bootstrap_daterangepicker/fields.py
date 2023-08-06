from django import forms
from django.core.exceptions import ValidationError
from django.utils import six
from django.utils.encoding import force_text
from django.utils.translation import string_concat, gettext_lazy as _

from .widgets import DateRangeWidget, DateTimeRangeWidget, DatePickerWidget


class AbstractRangeField(object):
    def to_python(self, value):
        # Try to coerce the value to unicode.
        unicode_value = force_text(value, strings_only=True)
        if isinstance(unicode_value, six.text_type):
            value = unicode_value.strip()
        else:
            raise ValidationError(
                _("Date range value: " + str(value) + " was not able to be converted to unicode.")
            )

        if self.widget.clearable:
            if value.strip() == '':
                return None, None

        if self.widget.separator in value:
            str_dates = value.split(self.widget.separator, 2)

            try:
                beginning = super().to_python(str_dates[0])
            except ValidationError as e:
                raise ValidationError(string_concat('Error in period beginning: ', e.message), e.code)

            try:
                end = super().to_python(str_dates[1])
            except ValidationError as e:
                raise ValidationError(string_concat('Error in period end: ', e.message), e.code)

            return beginning, end
        else:
            raise ValidationError(
                _("Invalid date range format."),
                code='invalid'
            )


class DateRangeField(AbstractRangeField, forms.DateField):
    widget = DateRangeWidget

    def __init__(self, clearable=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.clearable = clearable


class DateTimeRangeField(AbstractRangeField, forms.DateTimeField):
    widget = DateTimeRangeWidget

    def __init__(self, clearable=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.clearable = clearable


class DateField(forms.DateField):
    widget = DatePickerWidget

    def __init__(self, clearable=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.clearable = clearable
