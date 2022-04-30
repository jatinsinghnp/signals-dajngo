from django.utils import timezone
from django.db import models
from django.conf import settings
from django.utils.text import slugify


from django.dispatch import receiver
from django.db.models.signals import (
    post_save,
    pre_save,
    pre_delete,
    post_delete,
)


User = settings.AUTH_USER_MODEL
# Create your models here.


# @receiver(pre_save, sender=User)
# def user_presave_reciver(sender, instance, *args, **kwargs):

#     """
#     before save into the data base
#     """
#     print(instance.id,instance.username)


# @receiver(post_save, sender=User)
# def user_created_handler(sender, instance, created, *args, **kwargs):
#     """
#     after saved in  the data base
#     """
#     if created:
#         print("send email to", instance.username)
#     else:
#         print(instance.username, "was just created")


class BlogPost(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    linked = models.ManyToManyField(User, blank=True)
    notify_users = models.BooleanField(default=False)
    notify_users_timestamp = models.DateTimeField(
        blank=True, null=True, auto_now_add=False
    )
    active = models.BooleanField(default=True)


@receiver(pre_save, sender=BlogPost)
def blog_post_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


@receiver(post_save, sender=BlogPost)
def blog_post_post_save(sender, instance, created, *args, **kwargs):

    if instance.id and instance.notify_users:
        print("notify users")
        instance.notify_users = False
        instance.notify_users_timestamp = timezone.now()
        instance.save()


@receiver(pre_delete, sender=BlogPost)
def blog_post_pre_delete(sender, instance, *args, **kwargs):
    print(f"{instance.id} will be removed")


@receiver(post_delete, sender=BlogPost)
def blog_post_post_delete(sender, instance, *args, **kwargs):
    print(f"{instance.id} has removed")
