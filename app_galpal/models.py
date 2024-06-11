from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  first_name = models.TextField(max_length=200, null=True)
  last_name = models.TextField(max_length=200, null=True)
  display_name = models.CharField(max_length=30, null=True)
  bio = models.TextField(max_length=300, null=True)
  email = models.EmailField(max_length=254, unique=True, null=True)
  phone = models.IntegerField(unique=True, null=True)
  city = models.TextField(max_length=300, null=True, blank=True)
  state = models.TextField(max_length=300, null=True, blank=True)
  profile_photo = models.ImageField(upload_to='images/', null=True, blank=True) 
  #it is set to null and blank = true so that people can't do it, so maybe i need to make it something else

  def __str__(self):
    return self.user.username


class RequestedMatch(models.Model):
  Pending = "Pending"
  Approved = "Approved"
  Denied = "Denied"

  status_choices = {
    Pending: 'Pending',
    Approved: 'Approved',
    Denied: 'Denied'
  }
  requester = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='current_user')
  requested = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='requested_match')
  status = models.CharField(max_length=20, choices=status_choices, default=Pending)
  matched = models.BooleanField(default=False)

  def __str__(self):
    return f'Current User: {self.requester} Wants to Match With: {self.requested}'

#I think you could make a model called Friend List and create it when a match = true 

class Interests(models.Model):
  interests = models.CharField(max_length=150)

  def __str__(self):
    return self.interests

class InterestInventory(models.Model):
  user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='interest_inventory')
  interest = models.ForeignKey(Interests, on_delete=models.SET_NULL, null=True, related_name='interest')

  def __str__(self):
    return self.interest

# I'm nervous that message should come first with author content and time 

class MessageChannel(models.Model):
  name = models.CharField(max_length=200)
  user = models.ManyToManyField(Profile)

  def __str__(self):
    return f'Message Name: {self.name}, Users in Channel: {self.user} and {self.user}'

class Message(models.Model):
  message_channel = models.ForeignKey(MessageChannel, on_delete=models.CASCADE, related_name='channel')
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