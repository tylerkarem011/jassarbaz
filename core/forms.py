# core/forms.py
from django import forms
from .models import ClubMember

class ClubMemberForm(forms.ModelForm):
    class Meta:
        model = ClubMember
        fields = ['full_name', 'birth_date', 'student_id', 'group', 'photo']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }