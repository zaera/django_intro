from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from accounts.models import User


@receiver(pre_save, sender=User)
def pre_save_user(sender, instance, **kwargs):
    print('presave here') # noqa

    if instance.phone:
        instance.phone = ''.join(char for char in instance.phone if char.isdigit())

    if instance.email:
        instance.email = instance.email.lower()


# def username_check(sender, instance, **kwargs):
#     if User.objects.filter(username=instance.username.lower()).count():
#         raise ValidationError('Duplicate username')
#
#
# pre_save.connect(username_check, sender=User)


# @receiver(post_save, sender=User)
# def post_save_user_first(sender, instance, created, **kwargs):
#     if created:
#         print('post_save_user_first')
#
#
# @receiver(post_save, sender=User)
# def post_save_user_second(sender, instance, created, **kwargs):
#     if created:
#         print('post_save_user_second')


@receiver(pre_delete, sender=User)
def stop_delete(*args, **kwargs):
    raise DeleteIsNotAllowed('Instance could not be deleted')


class DeleteIsNotAllowed(Exception):
    pass
