from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db import transaction

from .models import Customer, Division, City, Zip

# call this UserAdminCreationForm, UserAdminChangeForm in your views.py


User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'password1',
        'placeholder': 'Enter password here'
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'password2',
        'placeholder': 'Enter same password here'
    }))

    class Meta:
        model = User
        fields = ['email', 'username']  # add the required field here

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")
        return cleaned_data

    # All emails are saved as lower case, lower case the email you get in the form and check
    # Otherwise it will be saved as new email same, but upper and lowercase mixtures
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return email
        # raise forms.ValidationError("Email already exists")
        self.add_error("email","Email already exists")


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'is_admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CustomerForm(UserAdminCreationForm):
    # Redesigned first_name, so I have to personally save it, must be here
    first_name = forms.CharField(required=False, label='First name', widget=forms.TextInput(attrs={
        'class': 'first_name',
        'id': 'first_name-id',
        'placeholder': 'Enter your code here'

    }))

    # Redesigned last_name, so I have to personally save it, must be here
    last_name = forms.CharField(required=False, label='Last name', widget=forms.TextInput(attrs={
        'class': 'zip_code',
        'id': 'zip-id',
        'placeholder': 'Enter last name here'

    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

        # name = models.CharField(null=False, blank=False)
        # user = models.OneToOneField(User, on_delete=models.CASCADE)
        # date_created = models.DateField(verbose_name='date joined',auto_now_add=True)
        # last_login = models.DateField(verbose_name=' last login', auto_now=True)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)  # stop save() # Model name of model but instance created
        # user.attributes=self.cleaned_data.get(' attributes ')
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        # student.attributes=self.cleaned_data.get(' attributes ')
        # Form must have this new attributes forms.charfield
        customer.first_name = self.cleaned_data.get('first_name')
        customer.last_name = self.cleaned_data.get('last_name')
        customer.save()
        return customer


class CustomerUpdateForm(forms.ModelForm):
    # Redesigned address, but I have to personally save it, must be above fields=[]
    address = forms.CharField(required=False, label='Address', widget=forms.Textarea(attrs={
        'rows': '2',
        'id': 'id_address',

    }))

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'division', 'city', 'zip', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()  # don't show anything city
        self.fields['zip'].queryset = Zip.objects.none()  # don't show anything city

        if self.instance.pk and self.instance.address:
            self.fields['address'].queryset = self.instance.address

        if 'division' in self.data:
            try:
                division_id = int(self.data.get('division'))
                self.fields['city'].queryset = City.objects.filter(division_id=division_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # For updating purpose
        elif self.instance.pk and self.instance.city:
            self.fields['city'].queryset = self.instance.division.city_set.all().order_by('name')

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['zip'].queryset = Zip.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # For updating purpose
        elif self.instance.pk and self.instance.zip:
            self.fields['zip'].queryset = self.instance.city.zip_set.all().order_by('name')
