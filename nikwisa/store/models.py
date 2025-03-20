from django.db import models
from django.apps import apps
from django.utils.text import slugify

# import users.models
# from django.contrib.auth import get_user_model
# from users.models import CustomUser as User


# User = get_user_model()

    # Add these models to your existing stores/models.py file
class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Province, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='areas')
    
    class Meta:
        unique_together = ('name', 'province')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Area, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}, {self.province.name}"

class Store(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, limit_choices_to={'role': 'merchant'})
    categories = models.ManyToManyField('categories.Category', related_name='stores', blank=True)
    
    event_planning_categories = models.ManyToManyField(
        'event_planning.EventPlanningCategories', 
        related_name="store_event_offerings", 
        blank=True
    )

    rent_hire_categories = models.ManyToManyField(
        'rent_hire.RentHireCategory',  # Reference to RentHireCategories model
        related_name="store_rent_offerings", 
        blank=True
    )

    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to='stores/', blank=True, null=True)
    overview = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    whats_app = models.CharField(max_length=255, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    reviews_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

     
    # Add these new fields
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, related_name='stores')
    service_areas = models.ManyToManyField(Area, related_name='serving_stores', blank=True)
    
    # New fields
    working_hours = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_responsive = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Store, self).save(*args, **kwargs)

    def update_rating(self):
        """Update the store's rating and reviews count."""
        reviews = self.reviews.all()
        self.reviews_count = reviews.count()
        self.rating = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0.0
        self.save()

    def __str__(self):
        return self.name
    



class StoreReview(models.Model):
    store = models.ForeignKey(Store, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', related_name="store_reviews", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(StoreReview, self).save(*args, **kwargs)
        self.store.update_rating()

    def delete(self, *args, **kwargs):
        store = self.store
        super(StoreReview, self).delete(*args, **kwargs)
        store.update_rating()

    def __str__(self):
        return f"Review by {self.user.username} on {self.store.name}"

class Reaction(models.Model):
    store = models.ForeignKey(Store, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', related_name="store_reactions", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.store.name}"

class Offering(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='offerings_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, related_name="offerings", on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', related_name="offerings", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    whatsapp_number = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StoreImage(models.Model):
    store = models.ForeignKey(Store, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.store.name} image"
    
