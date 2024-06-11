from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'

#########################################################################################################
class ProfileSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = Profile
    fields = ['id', 'first_name', 'last_name', 'user', 'email', 'phone', 'location', 'display_name', 'bio', 'profile_photo']

#########################################################################################################
class RequestedMatchSerializer(serializers.ModelSerializer):
  class Meta:
    model = RequestedMatch
    fields = ['user', 'matches']

#########################################################################################################
class InterestsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Interests
    fields = ['id', 'interests']

#########################################################################################################
class InterestInventorySerializer(serializers.ModelSerializer):
  interest = InterestsSerializer()

  class Meta:
    model = InterestInventory
    fields = ['user', 'interest']

#########################################################################################################
class MessageChannelSerializer(serializers.ModelSerializer):
  class Meta:
    model = MessageChannel
    fields = ['user', 'name']

#########################################################################################################
class MessageSerializer(serializers.ModelSerializer):
  message_channel = MessageChannelSerializer()

  class Meta:
    model = Message
    fields = ['message_channel', 'message_author', 'message_content', 'time']

#########################################################################################################
class MatchProfileQuestionsSerializer(serializers.ModelSerializer):
  class Meta:
    model = MatchProfileQuestions
    fields = ['id', 'question']

#########################################################################################################
class MatchProfileAnswersSerializer(serializers.ModelSerializer):
  question = MatchProfileQuestionsSerializer()

  class Meta:
    model = MatchProfileAnswers
    fields = ['user', 'question', 'answer', 'image_answer']

