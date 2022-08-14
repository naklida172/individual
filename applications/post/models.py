from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

User = get_user_model()


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} --> {self.date}'

    class Meta:
        ordering = ['id']


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField('like', default=False)

    def __str__(self):
        return f'{self.post}-{self.like}'


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    # rating = models.PositiveIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], default=0)


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating', verbose_name='ratings')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='rating', verbose_name='ratings')
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)

    def __str__(self):
        return f'{self.post} - {self.rating}'


class Favorite(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saves')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saves')
    favorite = models.BooleanField('save', default=False)
