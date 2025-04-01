from django import forms
from .models import User, OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreationForm(forms.ModelForm):
        password1 = forms.CharField(label=_('رمز عبور'), widget=forms.PasswordInput)
        password2 = forms.CharField(label=_('تکرار رمز عبور'), widget=forms.PasswordInput)

        class Meta:
            model = User
            fields = ('email', 'phone', 'username')


        def clean_password2(self):
            cd = self.cleaned_data

            if cd['password1'] != cd['password2']:
                raise ValidationError(_('پسورد شما یکی نمی‌باشد'))
            return cd['password2']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            if commit:
                user.save()
            return user


class UserChangeForm(forms.ModelForm):
        password = ReadOnlyPasswordHashField(help_text=_("you can change password using <a href=\"../password/\">this form</a>."))

        class Meta:
            model = User
            fields = ('email', 'phone', 'username', 'password', 'last_login')



class UserRegistrationForm(forms.Form):
        username = forms.CharField(label=_('نام کاربری'))
        phone = forms.CharField(max_length=11, label=_(' شماره همراه '))
        email = forms.EmailField(required=False, label=_('  ایمیل '))


        username.widget.attrs['class'] = 'form-control'
        phone.widget.attrs['class'] = 'form-control'
        email.widget.attrs['class'] = 'form-control'



        def clean_email(self):
            email = self.cleaned_data['email']
            user = User.objects.filter(email=email).exists()
            if user:
                raise ValidationError(_('با این ایمیل قبلا ثبت نام شده است'))
            return email

        def clean_phone(self):
            phone = self.cleaned_data['phone']
            user = User.objects.filter(phone=phone).exists()
            if user:
                raise ValidationError(_('با این شماره همراه قبلا ثبت نام شده است '))
            OtpCode.objects.filter(phone=phone).delete()
            return phone


class VerifyCodeForm(forms.Form):
        code = forms.IntegerField(label=_(' کد یکبار مصرف  '))

        code.widget.attrs['class'] = 'form-control'


class UserLoginForm(forms.Form):
        phone = forms.CharField( label=_(' شماره همراه '))

        phone.widget.attrs['class'] = 'form-control'
