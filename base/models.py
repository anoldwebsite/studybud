from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # In this app, a topic can have many rooms but a room can have onl one topic. If a topic is deleted, the rooms are not deleted but set to null.
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # A room can have many participants and a participant can be in many rooms.
    # The related_name attribute specifies the name of the reverse relation from the User model back to your model.
    # If you don't specify a related_name, Django automatically creates one using the name of your model with the suffix _set, for instance User.map_set.all().
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    # the auto_now will update the field every time the save method is called.
    updated = models.DateTimeField(auto_now=True)
    # The auto_now_add will set the timezone. now() only when the instance is created.
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ordering of the rooms shown wil be based on when they are updated and then when they are created.
        # - will reverse the order which without - is ascending order. With - the newest comes at the top.
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    # CASCADE means: If a user is deleted, delete all her messages too.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # CASCADE means: If the instance of class/Model Room in which this message exists is deleted, delete the messages in that room too.
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    # the auto_now will update the field every time the save method is called.
    updated = models.DateTimeField(auto_now=True)
    # The auto_now_add will set the timezone. now() only when the instance is created.
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        # Show only the first 50 characters of a message.
        return self.body[0:50]
