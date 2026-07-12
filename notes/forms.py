from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    """Form used to create and update sticky notes."""

    class Meta:
        model = Note
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter a note title",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your note here",
                    "rows": 8,
                }
            ),
        }
