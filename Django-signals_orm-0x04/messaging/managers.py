from django.db import models


class UnreadMessagesManager(models.Manager):
    """
    Custom manager that returns unread messages for a specific user.
    The view can further optimize the returned queryset (select_related, only, etc).
    """

    def unread_for_user(self, user):
        """
        Return a queryset of unread Message instances for `user`.
        """
        return self.get_queryset().filter(receiver=user, read=False)

