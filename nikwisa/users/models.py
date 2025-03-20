from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'client')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Basic Information
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    
    # User Type and Status
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('merchant', 'Merchant'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    user_type = models.CharField(max_length=50, blank=True, null=True)
    # Verification Status
    is_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    profile_completion = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # System Fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Contact Information
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    
    # Address Information
    address_line = models.TextField(blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    

    
    # notification_preferences = models.JSONField(default=dict, blank=True, null=True)
    
    # Social Media (Personal)
    facebook_profile = models.URLField(max_length=200, blank=True, null=True)
    instagram_handle = models.CharField(max_length=30, blank=True, null=True)
    twitter_handle = models.CharField(max_length=30, blank=True, null=True)
    linkedin_profile = models.URLField(max_length=200, blank=True, null=True)
    
    # Security and Activity
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    last_password_change = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    
    # Media
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    
    # Documents
    id_proof_type = models.CharField(max_length=50, blank=True, null=True)
    id_proof_number = models.CharField(max_length=50, blank=True, null=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    class Meta:
        indexes = [
            models.Index(fields=['email', 'username']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['role']),
        ]

class StoredJWT(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="jwt_token")
    access_token = models.TextField()
    refresh_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"JWT for {self.user.username}"
    
# Message Model
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

# Like Model
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    target_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="likes_received")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'target_user')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user} liked {self.target_user}"

# Review Model
class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reviewed_user = models.ForeignKey(CustomUser, related_name='reviews_received', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'reviewed_user')  # One review per user

    def __str__(self):
        return f"Review by {self.user}"
    
