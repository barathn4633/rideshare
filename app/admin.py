from django.db import transaction
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.html import escape
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, Vehicle, VehicleSharing, Request, Message, Follow, Profile, DriverInfo

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())


class CustomUserAdmin(admin.ModelAdmin):
    """
    The default UserAdmin class, but with changes for our CustomUser
    where `first_name` and `last_name` are replaced by `full_name` and
    `short_name`
    """
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('full_name', 'short_name', 'email', 'sex', 'phone_number','wallet_address','private_key', 'user_type', 'address')}),
        (_('Permissions'), {'fields': ('is_active','is_verified', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
         ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email', 'full_name', 'user_type', 'is_staff','last_login','date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups','is_verified')
    search_fields = ('username', 'full_name', 'short_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(CustomUserAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults.update({
                'form': self.add_form,
            })
        defaults.update(kwargs)
        return super(CustomUserAdmin, self).get_form(request, obj, **defaults)

    def get_urls(self):
        from django.conf.urls import url
        urlpatterns = [

    url(r'^(\d+)/password/$', self.admin_site.admin_view(self.user_change_password)),


]+ super(CustomUserAdmin, self).get_urls()
        return urlpatterns

    def lookup_allowed(self, lookup, value):
        # See #20078: we don't want to allow any lookups involving passwords.
        if lookup.startswith('password'):
            return False
        return super(CustomUserAdmin, self).lookup_allowed(lookup, value)

    @sensitive_post_parameters_m
    @csrf_protect_m
    @transaction.atomic
    def add_view(self, request, form_url='', extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):
            if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404(
                    'Your user does not have the "Change user" permission. In '
                    'order to add users, Django requires that your user '
                    'account have both the "Add user" and "Change user" '
                    'permissions set.')
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        username_field = self.model._meta.get_field(self.model.USERNAME_FIELD)
        defaults = {
            'auto_populated_fields': (),
            'username_help_text': username_field.help_text,
        }
        extra_context.update(defaults)
        return super(CustomUserAdmin, self).add_view(request, form_url,
                                                     extra_context)

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.queryset(request), pk=id)
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                msg = ugettext('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
        }
        return TemplateResponse(request,
                                self.change_user_password_template or
                                'admin/auth/user/change_password.html',
                                context, current_app=self.admin_site.name)

    def response_add(self, request, obj, post_url_continue=None):
        """
        Determines the HttpResponse for the add_view stage. It mostly defers to
        its superclass implementation but is customized because the User model
        has a slightly different workflow.
        """
        # We should allow further modification of the user just added i.e. the
        # 'Save' button should behave like the 'Save and continue editing'
        # button except in two scenarios:
        # * The user has pressed the 'Save and add another' button
        # * We are adding a user in a popup
        if '_addanother' not in request.POST and '_popup' not in request.POST:
            request.POST['_continue'] = 1
        return super(CustomUserAdmin, self).response_add(request, obj,
                                                         post_url_continue)


admin.site.register(CustomUser, CustomUserAdmin)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ( 'make', 'model', 'user','seats', 'type', 'category')
    list_filter = ('category','type','year')
admin.site.register(Vehicle,VehicleAdmin),


class VehicleShareAdmin(admin.ModelAdmin):
    list_display = ('start', 'dest', 'cost', 'date', 'start_time', 'arrival_time', 'no_pass', 'sex')
    list_filter = ('date','ended','no_pass')
admin.site.register(VehicleSharing,VehicleShareAdmin)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('user','reg_date','ride','bearable','status','payment_made','tx_id')
    list_filter = ('ride','status','reg_date')
admin.site.register(Request,RequestAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('recipient','sender','message','date','read')
    list_filter = ('recipient','sender','date')

admin.site.register(Message,MessageAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('followee','follower','time')
    list_filter = ('follower','followee','time')

admin.site.register(Follow,FollowAdmin)

admin.site.register(Profile)

class DriverInfoAdmin(admin.ModelAdmin):
    list_display = ('driver','liscence_no','date_issuance')
    list_filter = ('confirmed','date_issuance')

admin.site.register(DriverInfo,DriverInfoAdmin)
