from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Address(models.Model):
    street = models.CharField(max_length=80)
    suite = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    zipcode = models.CharField(max_length=10)

    class Meta:
        ordering = ('zipcode',)
    
    def __str__(self):
        return self.zipcode

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")

    class Meta:
        ordering = ('id',)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=100) 
    email = models.EmailField()
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        ordering = ('id',)
    
    def __str__(self):
        return self.name