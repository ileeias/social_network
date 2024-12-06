from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        if phone_number is None:
            raise ValueError('Phone Number is required!')
        if len(str(phone_number)) < 10:
            raise ValueError('Укажите полный номер!')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)
class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    bio = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    residence = models.CharField(max_length=225)
    hobbies = models.TextField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='users')
    date_joined = models.DateTimeField(auto_now_add=True)
    friends = models.ManyToManyField('CustomUser', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.name} {self.surname}, номер: {self.phone_number}"

class Friends(models.Model):
    from_user = models.ForeignKey('CustomUser', related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey('CustomUser', related_name='to_user', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[
        ('no_request', 'No_request❌'),
        ('accepted', 'Accepted✅'), # Принял
        ('rejected', 'Rejected❎'), # Отклонил
    ])

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.get_status_display()})"

class Posts(models.Model):
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='posts')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    comment = models.ManyToManyField('Comments', null=True, blank=True)
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.author.name} написал "{self.title}"'

class Comments(models.Model):
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='comments')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.author} прокоментировал запись "{self.post}"'

class Likes(models.Model):
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} понравился {self.post}"

class Dislikes(models.Model):
    post = models.ForeignKey('Posts', on_delete=models.CASCADE)
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} не понравился {self.post}"