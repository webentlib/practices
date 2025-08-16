from django.db import models


class AdmUser(models.Model):
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login_attempt_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
