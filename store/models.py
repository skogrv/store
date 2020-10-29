from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_currentuser.db.models import CurrentUserField
from django.core.validators import MaxLengthValidator, MinLengthValidator
from star_ratings.models import Rating

Rating_CHOICES = (
    (1, '>*'),
    (2, '*'),
    (3, '*'),
    (4, '*'),
    (5, '*')
)


class Comment(models.Model):
    post = models.ForeignKey("Listing", on_delete=models.CASCADE, null=True, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    comment = models.TextField(max_length=300)
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    liked = models.ManyToManyField(User, related_name='liked', blank=True)
    is_liked = models.BooleanField(default=True)
    rating = models.IntegerField()


    class Meta:
        ordering = ['-created_on']



class Listing(models.Model):
    listing_images = models.ForeignKey('ListingImage', on_delete=models.CASCADE, null=True, related_name='related_images')
    title = models.CharField(max_length=30)
    description = models.TextField(validators=[MaxLengthValidator(400), MinLengthValidator(100)])
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)
    price = models.CharField(max_length=4)
    main_image = models.ImageField(upload_to='media')
    auth = CurrentUserField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('store-home')


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to='media')


