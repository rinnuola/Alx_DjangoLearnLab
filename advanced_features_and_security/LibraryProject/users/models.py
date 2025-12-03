from django.contrib.auth.models import AbstractBaseUser

class CustomUser(AbstractBaseUser):
    email =
models.EmailField(unique=True)
    phone_number =
models.CharField(max_length=20)
    # ... additional fields and methods as required ...