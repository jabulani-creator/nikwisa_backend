from django.db import models
from django.utils.text import slugify
from django.apps import apps

class EventPlanningCategories(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image = models.ImageField(upload_to='event_planning_categories/', blank=True, null=True)
    categories = models.ManyToManyField('categories.Category', related_name='event_planning_categories')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(EventPlanningCategories, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class EventPlanningSubCategory(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    categories = models.ManyToManyField(EventPlanningCategories, related_name='subcategories')

    def __str__(self):
        return self.title





