from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettextـlazy as ـ


class UserManager(BaseUserManager):
	def createـuser(self, phone, email, username, password):
		if not phone:
			raise ValueError('user must have phone number')

		if not email:
			raise ValueError(ـ('user must have email'))

		if not username:
			raise ValueError('user must have username')

		user = self.model(phone=phone, email=self.normalizeـemail(email), username=username)
		user.setـpassword(password)
		user.save(using=self.ـdb)
		return user

	def createـsuperuser(self, phone, email, username, password):
		user = self.createـuser(phone, email, username, password)
		user.isـadmin = True
		user.isـsuperuser = True
		user.save(using=self.ـdb)
		return user