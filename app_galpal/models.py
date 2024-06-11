from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  first_name = models.TextField()
  last_name = models.TextField()
  display_name = models.CharField(max_length=30)
  bio = models.TextField(max_length=300)
  email = models.EmailField(max_length=254)
  phone = models.IntegerField(max_length=13)
  location = models.TextField(max_length=300, null=True, blank=True)
  profile_photo = models.ImageField(upload_to='images/', null=True, blank=True) 
  #it is set to null and blank = true so that people can't do it, so maybe i need to make it something else

  def __str__(self):
    return self.user.username

class RequestedMatch(models.Model):
  user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='current_user')
  matches = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='requested_match')

  def __str__(self):
    return f'Current User: {self.user} Wants to Match With: {self.matches}'

# you might need to make a model called like 'Matched' with a boolean field to identify whether or not these users are matched? 

class Interests(models.Model):
  interests = models.CharField(max_length=150)

  def __str__(self):
    return self.interests

class InterestInventory(models.Model):
  user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='interest_inventory')
  interest = models.ForeignKey(Interests, on_delete=models.SET_NULL, null=True, related_name='interest')

  def __str__(self):
    return self.interest

class MessageChannel(models.Model):
  name = models.CharField(max_length=200, related_name='message_channel')
  user = models.ManyToManyField(Profile)

  def __str__(self):
    return f'Message Name: {self.name}, Users in Channel: {self.user} and {self.user}'

class Message(models.Model):
  message_channel = models.ForeignKey(MessageChannel, on_delete=models.CASCADE, related_name='message_channel')
  message_author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='message')
  message_content = models.TextField(max_length=500)
  time = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Channel: {self.message_channel}, Message Author: {self.message_author}, Message: {self.message_content}, Sent: {self.time}'
  
class MatchProfileQuestions(models.Model):
  question = models.CharField(max_length=250)

  def __str__(self):
    return f'Question: {self.question}'

class MatchProfileAnswers(models.Model):
  user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='profile_answers')
  question = models.ForeignKey(MatchProfileQuestions, on_delete=models.SET_NULL, null=True)
  answer = models.TextField(max_length=300, null=True, blank=True)
  image_answer = models.ImageField(upload_to='images/', null=True, blank=True)

  def __str__(self):
    return f'User: {self.user}, Question: {self.question}, Answer: {self.answer} {self.image_answer}'