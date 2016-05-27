from django import forms
from postIssue.models import MyUser
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100);
    password = forms.CharField(widget=forms.PasswordInput);

    def __init__(self, *args, **kwargs):
        self.authenticated_user=None
        super(LoginForm,self).__init__(*args,**kwargs)

    def clean_username(self):
        data_username = self.cleaned_data['username']
        if MyUser.objects.filter(username=data_username).count()!=1:
            raise forms.ValidationError('Invalid username')
        return data_username;

    def clean(self):
        data_username = self.cleaned_data.get('username','')
        data_passwd = self.cleaned_data.get('password','')
        user = authenticate(username=data_username, password=data_passwd)
        if data_username and data_passwd and not user:
            raise forms.ValidationError('Username /Password does not match');
        if user.is_active == False:
            raise forms.ValidationError('Inactive User')
        self.authenticated_user=user;
        return self.cleaned_data;


class SignUpForm(forms.ModelForm):

    password = forms.CharField(max_length = 20, widget = forms.PasswordInput);
    confirm_password = forms.CharField(max_length = 20, widget = forms.PasswordInput);

    def clean_confirm_password(self):
        data_password = self.cleaned_data.get('password','')
        data_confirm_password = self.cleaned_data.get('confirm_password','')

        if (data_password and data_confirm_password 
                and data_confirm_password!=data_password):
            raise forms.ValidationError('The 2 passwords did not match')
        return data_password;

    def clean_email(self):
        data_email = self.cleaned_data.get('email','')

        if not data_email:
            raise forms.ValidationError('This field is required');
        #if MyUser.objects.filter(email=data_email).exists():
            #raise forms.ValidationError('User with this email already exists');
        return data_email;



    class Meta:
        model = MyUser
        fields = ['username', 'email', 'phone', 'first_name', 'last_name', 'profile_pic']

   


               


class ForgotPassword(forms.Form):
    username = forms.CharField(max_length=100);

    def clean_username(self):
        data_username = self.cleaned_data.get('username','')
        if data_username and not MyUser.objects.filter(username=data_username).exists():
            raise forms.ValidationError('Invalid username')
        return data_username;

class SetPassword(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput)

    def clean_confirm_new_password(self):
        data_new_password = self.cleaned_data.get('new_password','')
        data_confirm_new_password = self.cleaned_data.get('confirm_new_password','')

        if (data_new_password and data_confirm_new_password 
                and data_confirm_new_password!=data_new_password):
            raise forms.ValidationError('The 2 passwords did not match')
        return data_new_password;