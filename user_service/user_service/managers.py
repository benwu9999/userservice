from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, userId, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        if not (userId and email):
            raise ValueError('The given userId and email must be set')
        user = self.model(userId=userId, email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_user(self, userId, email, password=None, **extra_fields):
        return self._create_user(userId, email, password, **extra_fields)


