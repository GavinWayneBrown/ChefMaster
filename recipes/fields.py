# fields.py

from django import forms
from datetime import timedelta

class CustomDurationField(forms.DurationField):
    def to_python(self, value):
        if value in self.empty_values:
            return None
        if isinstance(value, timedelta):
            return value
        try:
            hours, minutes = map(int, value.split(':'))
            return timedelta(hours=hours, minutes=minutes)
        except (ValueError, TypeError):
            raise forms.ValidationError(self.error_messages['invalid'], code='invalid')