from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    institution = forms.CharField(max_length=100, required=True)
    course_of_study = forms.CharField(max_length=100, required=True)
    year_of_study = forms.CharField(max_length=20, required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 
                 'institution', 'course_of_study', 'year_of_study', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.institution = self.cleaned_data['institution']
        user.course_of_study = self.cleaned_data['course_of_study']
        user.year_of_study = self.cleaned_data['year_of_study']
        user.user_type = 'student'
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 
                 'institution', 'course_of_study', 'year_of_study', 'profile_picture']