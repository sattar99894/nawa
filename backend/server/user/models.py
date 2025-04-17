"""
 مدل های مربوط به اکانت یوزر ها و اطلاعات اصلی آنها
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
from django_jalali.db import models as jmodels
from shop.models import Product
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractBaseUser):
        """
        مدل های مربوط به اکانت یوزر ها و اطلاعات اصلی آنها
        """
        username = models.CharField(max_length=250,verbose_name=_('username'),null=True,blank=True)
        email = models.EmailField(null=True,blank=True,verbose_name=_('email'))
        phone = models.CharField(unique=True,max_length=11,verbose_name=_('phone')) 

        is_active = models.BooleanField(default=True)
        is_admin = models.BooleanField(default=False)
        likes = models.ManyToManyField(Product, blank=True, related_name='likes')
        # set a manager role for shop manager to access orders and products
        is_manager = models.BooleanField(default=False)
        created_at = jmodels.jDateTimeField(auto_now_add=True,verbose_name=_('زمان عضویت'))
        updated_at = jmodels.jDateTimeField(auto_now=True,verbose_name=_('زمان آخرین تغییرات'))

        USERNAME_FIELD = 'phone'
        REQUIRED_FIELDS = ['username', 'email']
        objects = UserManager()

        class Meta:
            verbose_name = _('کاربر')
            verbose_name_plural = _('کاربرها')


        def __str__(self):
            return str(self.phone)

        def has_perm(self,perm,obj=None):
            return True

        def has_module_perms(self,app_label):
            return True

        @property
        def is_staff(self):
            return self.is_admin

        def get_likes_count(self):
            return self.likes.count()


class OtpCode(models.Model):
        """
        در این مدل ما برای ایجاد کد یکبار مصرف سه پارامتر طمان تولید و شماره همراه و کد را در نظر گرفته ایم 
        
        که برای اینکه نمی‌دانیم فرد ثبت نام کرده است یا نه 
        و بخاطر استفاده از روش کلاس در ویو و سرعت کار از چرکتر فیلد برای شماره همراه استفاده شده است 
        """    
        phone = models.CharField(max_length=11, unique=True)
        code = models.PositiveSmallIntegerField()

        created = models.DateTimeField(auto_now=True)

        def __str__(self):
            return f'{self.phone} - {self.code} - {self.created}'
        

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    address = models.CharField(max_length=900)

    

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = _('آدرس ها')