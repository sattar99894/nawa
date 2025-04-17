from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
	def create_user(self, phone, email, username, password):
		if not phone:
			raise ValueError(_('داشتن  شماره همراه برای کاربر ضروری است'))

		if not email:
			raise ValueError(_('داشتن ایمیل برای کاربر ضروری است'))

		if not username:
			raise ValueError(_('داشتن نام کاربری برای کاربر ضروری است'))

		user = self.model(phone=phone, email=self.normalize_email(email), username=username)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, phone, email, username, password):
		user = self.create_user(phone, email, username, password)
		user.is_admin = True
		user.is_superuser = True
		user.save(using=self._db)
		return user