from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.conf import settings
import os
import shutil

# Usually pre_delete is used to clean up, the folder after delete() is clicked


# as the instance still exist after the save()
def delete_folder(sender, instance, *args, **kwargs):
    try:  # instance.profile_image.delete()  will delete your default.png
        path = os.path.join(os.getcwd(), f'media\profile_images\{instance.pk}')
        shutil.rmtree(path)

    except OSError:
        pass


pre_save.connect(delete_folder, sender=settings.AUTH_USER_MODEL)

# signal does not work when using it in a separate file
