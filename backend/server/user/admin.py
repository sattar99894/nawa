from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import OtpCode
from django.contrib.auth import get_user_model
# from core.models import Order

User = get_user_model()

# class OrderInline(admin.TabularInline):
# 	model = Order
# 	raw_id_fields = ('product',)

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
	list_display = ('phone', 'code', 'created')


class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('email', 'phone', 'is_admin')
	list_filter = ('is_admin',)
	readonly_fields = ('last_login',)

	fieldsets = (
		('Main', {'fields':('email', 'phone', 'username', 'password')}),
		('Permissions', {'fields':('is_active', 'is_admin','last_login')}),
	)

	add_fieldsets = (
		(None, {'fields':('phone', 'email', 'username', 'password1', 'password2')}),
	)
	# inlines = (OrderInline,)

	search_fields = ('email', 'username')
	ordering = ('username',)
	filter_horizontal = ()


admin.site.register(User, UserAdmin)