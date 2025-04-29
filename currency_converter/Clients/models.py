from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth import get_user_model

class CustomClientManager(BaseUserManager):
    """
    Custom manager for Client model.
    """
    def create_user(self,email,password=None,**extra_fields):
        """
        Create and return a user with an email address and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        ClientModel = get_user_model()
        client = ClientModel(email=email, **extra_fields)
        client.set_password(password)
        client.save(using=self._db)

        return client
    
    def create_superuser(self,email,password=None,**extra_fields):
        """
        Create and return a superusser with an email address and password.
        """
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_active",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if not email:
            raise ValueError("The Email field must be set")
        return self.create_user(email,password,**extra_fields)
    
class Client(AbstractUser):
    """
    Named Client. The Client model extends the AbstractUser model to make email the Username field.
    The name client was chosen as an umbrella term to cover both individuals and companies who wish to use the API services.
    The Client model is used to store information about the clients who will be using the API services.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True,help_text="Enter your Email address")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #since we use the emal as username we should verify the email
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)
    email_verification_token_expires = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(
        ("verified"),
        default=False,
        help_text=("Designates whether the CLient has verified their email address.")
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomClientManager()

    def __str__(self):
        return self.email
