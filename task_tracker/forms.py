from datetime import datetime, date
from django import forms
from .models import Task


# Форма задачи
class TaskForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(
        format=('%Y-%m-%d')))
    start_time = forms.TimeField()
    end_date = forms.DateField(widget=forms.DateInput(
        format=('%Y-%m-%d')), required=False)
    end_time = forms.TimeField(required=False)
    planned_end_date = forms.DateField(
        widget=forms.DateInput(format=('%Y-%m-%d')))
    planned_end_time = forms.TimeField()

    class Meta:
        model = Task
        fields = [
            'title', 'description', 'performer',
            'observers', 'start_date', 'start_time',
            'end_date', 'end_time', 'status',
            'planned_end_date', 'planned_end_time',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs['instance']:
            self.fields['start_date'].initial = \
                kwargs['instance'].start_datetime.date()
            self.fields['start_time'].initial = \
                kwargs['instance'].start_datetime.time()
            if self.fields['end_date'].initial and self.fields['end_time'].initial:
                self.fields['end_date'].initial = \
                    kwargs['instance'].end_datetime.date()
                self.fields['end_time'].initial = \
                    kwargs['instance'].end_datetime.time()
            self.fields['planned_end_date'].initial = \
                kwargs['instance'].planned_end_datetime.date()
            self.fields['planned_end_time'].initial = \
                kwargs['instance'].planned_end_datetime.time()
        else:
            self.fields['start_date'].initial = date.today()
            self.fields['start_time'].initial = datetime.now().time()

    def save(self, commit=True):
        end_datetime = None
        start_datetime = datetime.combine(self.cleaned_data['start_date'],
                                          self.cleaned_data['start_time'])
        if self.cleaned_data['end_date'] and self.cleaned_data['end_time']:
            end_datetime = datetime.combine(self.cleaned_data['end_date'],
                                            self.cleaned_data['end_time'])
        planned_end_datetime = datetime.combine(
            self.cleaned_data['planned_end_date'],
            self.cleaned_data['planned_end_time'])
        form = super(TaskForm, self).save(commit=False)
        form.start_datetime = start_datetime
        form.end_datetime = end_datetime
        form.planned_end_datetime = planned_end_datetime
        if commit:
            form.save()
            self.save_m2m()
        return form
