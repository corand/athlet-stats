from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserProfileUserManager(BaseUserManager):
    def create_user(self,email,password=None):
        if not email:
            msg = "Users must have an email address"
            raise ValueError(msg)
        user = self.model(email=UserProfileUserManager.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        user = self.create_user(email,password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user




GENDER_CHOICES = (
    (1, 'Hombre'),
    (2, 'Mujer'),
)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email address",max_length=255,unique=True,db_index=True)    
    profile_picture = models.ImageField(_("profile_picture"),blank=True,null=True,upload_to="profiles/")
    name = models.CharField(_("name"),max_length=30,blank=True,null=True)
    first_surname = models.CharField(_("first_surname"),max_length=30,blank=True,null=True)
    second_surname = models.CharField(_("second_surname"),max_length=30,blank=True,null=True)
    gender = models.IntegerField(max_length=30,choices=GENDER_CHOICES,blank=True,null=True)  
    self_description_es = models.TextField(_("self_description_es"),blank=True,null=True)
    self_description_eu = models.TextField(_("self_description_eu"),blank=True,null=True)
    coach_description = models.TextField(_("coach_description"),blank=True,null=True)
    slug = models.SlugField(blank=True,null=True)
    twitter = models.URLField(blank=True,null=True)
    
    USERNAME_FIELD = "email"

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileUserManager()

    def get_short_name(self):
        return "%s %s" % (self.name,self.first_surname)

    def get_full_name(self):
        return "%s %s %s" % (self.name,self.first_surname,self.second_surname)

    def __unicode__(self):
        return self.email
