from django import forms
from .models import Task
from datetime import date


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional description'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    # 🔹 Strong title validation
    def clean_title(self):
        title = self.cleaned_data.get('title')

        if not title or not title.strip():
            raise forms.ValidationError('Title cannot be empty.')

        return title.strip()

    # 🔹 Business logic validation
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')

        if due_date and due_date < date.today():
            raise forms.ValidationError('Due date cannot be in the past.')

        return due_date