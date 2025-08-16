from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.users.models import User


class CustomAuthenticationForm(AuthenticationForm):
    @staticmethod
    def _check_failed_login_attempts(user):
        if user and user.failed_login_attempts > 5:
            raise ValidationError('Too many failed login attempts')

    def get_invalid_login_error(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()

        if user:
            user.failed_login_attempts += 1
            user.last_failed_login_attempt_at = timezone.now()
            user.save()

        self._check_failed_login_attempts(user)
        return super().get_invalid_login_error()

    def confirm_login_allowed(self, user):
        self._check_failed_login_attempts(user)
        return super().confirm_login_allowed(user)
