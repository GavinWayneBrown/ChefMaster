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
        
    def prepare_value(self, value):
        if isinstance(value, timedelta):
            total_seconds = int(value.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}"
        return value
    