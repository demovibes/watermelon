from django.db import models


class Message(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,
        help_text="User who posted the message")
    time = models.DateTimeField(auto_now_add=True,
        help_text="Time the message was posted")
    text = models.CharField(max_length=255,
        help_text='Chat message text')

    def __str__(self):
        return ("(%s) %s: %s") % (self.time, self.user.get_username(), self.text)
