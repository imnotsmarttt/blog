from django import forms

from .models import Blog


class CreateBlogForm(forms.ModelForm):
    """Форма создания блога"""
    class Meta:
        model = Blog
        fields = ['name', 'description', 'rubric']
        labels = {
            'name': '',
            'description': '',
            'rubric': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form_input', 'placeholder': 'Введите название блога'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form_textarea', 'placeholder': 'Описание блога (про что)'
            }),
            'rubric': forms.Select(attrs={
                'class': 'form_choice'
            }),
        }
