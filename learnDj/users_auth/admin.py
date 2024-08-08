from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'date_of_birth', 'groups')

    def clean_groups(self):
        groups = self.cleaned_data.get('groups')
        group_names = [group.name for group in groups]

        if 'Paid' in group_names and 'Trial' in group_names:
            raise ValidationError("Groups contradiction!!!")
        if 'Minor' in group_names and 'Adult' in group_names:
            raise ValidationError("Groups contradiction!!!")

        return groups


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username', 'email', 'date_of_birth', 'password', 'groups', 'user_permissions')

    def clean_groups(self):
        groups = self.cleaned_data.get('groups')
        group_names = [group.name for group in groups]

        if 'Paid' in group_names and 'Trial' in group_names:
            raise ValidationError("Groups contradiction!!!")
        if 'Minor' in group_names and 'Adult' in group_names:
            raise ValidationError("Groups contradiction!!!")

        return groups

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'date_of_birth', 'is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'date_of_birth', 'groups')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)