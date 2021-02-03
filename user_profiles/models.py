from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    User profiles are an extension to the built-in user auth model, linked by
    a OneToOne field.  Profiles allow a user to add extra information, such as
    a short biography, location, birhdate etc.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,
        help_text="The auth.User model this profile is linked to")

    image = models.ImageField(upload_to='user_profiles/', max_length=255, blank=True, null=True,
        help_text="Picture of the user")

    bio = models.TextField(max_length=500, blank=True,
        help_text="A short biography about the user")
    location = models.CharField(max_length=50, blank=True,
        help_text='Custom location field, e.g. "USA" or "London"')
    birth_date = models.DateField(null=True, blank=True,
        help_text="User's birthday")

    theme = models.FilePathField(max_length=255, blank=True, path='css/theme', match='\.css$',
        help_text="Custom theme - choice of CSS files in css/theme directory")

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('user_profiles:profile-detail', kwargs={'slug': self.user.username})

    class Meta:
        ordering = ['-user__is_superuser', '-user__is_staff', 'user__username']

    def __str__(self):
        return '%s [%s]' % (self.user, self.location)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
