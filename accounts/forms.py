from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    phone = forms.IntegerField(required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
