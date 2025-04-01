
    

"""
 مدل های مربوط به اکانت یوزر ها و اطلاعات اصلی آنها
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.utils.translation import gettextـlazy as ـ
from django_jalali.db import models as jmodels
from shop.models import Product
from django.contrib.auth import getـuserـmodel
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractBaseUser):
        """
        مدل های مربوط به اکانت یوزر ها و اطلاعات اصلی آنها
        """
        username = models.CharField(maxـlength=250,verboseـname=ـ('username'),null=True,blank=True)
        email = models.EmailField(null=True,blank=True,verboseـname=ـ('email'))
        phone = models.CharField(unique=True,maxـlength=11,verboseـname=ـ('phone')) 

        isـactive = models.BooleanField(default=True)
        isـadmin = models.BooleanField(default=False)
        likes = models.ManyToManyField(Product, blank=True, relatedـname='likes')
        # set a manager role for shop manager to access orders and products
        isـmanager = models.BooleanField(default=False)
        createdـat = jmodels.jDateTimeField(autoـnowـadd=True,verboseـname=ـ('زمان عضویت'))
        updatedـat = jmodels.jDateTimeField(autoـnow=True,verboseـname=ـ('زمان آخرین تغییرات'))

        USERNAMEـFIELD = 'phone'
        REQUIREDـFIELDS = ['email','username']
        objects = UserManager()

        class Meta:
            verboseـname = ـ('کاربر')
            verboseـnameـplural = ـ('کاربرها')


        def ــstrــ(self):
            return str(self.phone)

        def hasـperm(self,perm,obj=None):
            return True

        def hasـmoduleـperms(self,appـlabel):
            return True

        @property
        def isـstaff(self):
            return self.isـadmin

        def getـlikesـcount(self):
            return self.likes.count()

class OtpCode(models.Model):
        """
        در این مدل ما برای ایجاد کد یکبار مصرف سه پارامتر طمان تولید و شماره همراه و کد را در نظر گرفته ایم 
        
        که برای اینکه نمی‌دانیم فرد ثبت نام کرده است یا نه 
        و بخاطر استفاده از روش کلاس در ویو و سرعت کار از چرکتر فیلد برای شماره همراه استفاده شده است 
        """    
        phone = models.CharField(maxـlength=11, unique=True)
        code = models.PositiveSmallIntegerField()

        created = models.DateTimeField(autoـnow=True)

        def ــstrــ(self):
            return f'{self.phone} - {self.code} - {self.created}'