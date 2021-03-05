from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, phone, first_name, last_name, password=None):
        if not phone:
            raise ValueError('لطفا شماره موبایل خود را وارد کنید.')
        else:
            user = self.model(
                phone=phone,
                first_name=first_name,
                last_name=last_name

            )
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, phone, first_name, last_name, password=None):
        user = self.create_user(
            phone=phone,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = None
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=200)
    phone_regex = RegexValidator(regex=r'^09(\d{9})$',
                                 message="Phone number must be entered in the format: '09111111111'")
    phone = models.CharField(validators=[phone_regex], max_length=11, unique=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    # cart_number = models.PositiveBigIntegerField(null=True, blank=True)  # shomare cart banki
    birth_day = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def is_staff(self):
        return self.is_admin


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r'^09(\d{9})$',
                                 message="Phone number must be entered in the format: '09111111111'")
    phone = models.CharField(validators=[phone_regex], max_length=11, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    Count = models.IntegerField(default=0, help_text='Number of otp sent')
    logged = models.BooleanField(default=False, help_text='If otp verification got successful')
    forgot = models.BooleanField(default=False, help_text='only true for forgot password')
    forgot_logged = models.BooleanField(default=False, help_text='Only true if validate otp forgot get successful')

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    province = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    address = models.TextField()
    post_code = models.PositiveBigIntegerField()  # code posti khone

    def __str__(self):
        return self.user

    class Meta:
        verbose_name_plural = 'Addresses'
