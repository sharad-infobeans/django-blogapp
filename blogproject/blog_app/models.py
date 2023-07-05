from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    # Add any additional attributes you want
    social_handle = models.URLField(blank=True)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option=”build_ext” --global-option=”--disable-jpeg”
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    profession = models.CharField(max_length=100,blank=True)
    profile_bio = models.CharField(max_length=100,blank=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username

class BlogPosts(models.Model):
    blog_title = models.CharField(max_length=100)
    blog_content = RichTextField()
    blog_image = models.ImageField(upload_to='blogs',blank=True)
    blog_created_date = models.DateTimeField(default=timezone.now)
    blog_published_date = models.DateTimeField(blank=True, null=True)
    blog_author = models.ForeignKey(User,related_name='author',on_delete=models.CASCADE)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("blog_app:detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.blog_title