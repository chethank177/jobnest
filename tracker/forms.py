from django import forms
from .models import JobApplication
import datetime

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['company', 'role', 'date_applied', 'status', 'job_url', 'notes']
        widgets = {
            'date_applied': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_date_applied(self):
        date_applied = self.cleaned_data['date_applied']
        if date_applied > datetime.date.today():
            raise forms.ValidationError('Application date cannot be in the future.')
        return date_applied 