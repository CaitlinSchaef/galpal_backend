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
    fields = ['id', 'first_name', 'last_name', 'user', 'email']

#########################################################################################################
class RequestedMatchSerializer(serializers.ModelSerializer):
  class Meta:
    model = RequestedMatch
    fields = ['requester', 'requested', 'status', 'matched', 'status_choices']

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

#########################################################################################################
class MatchProfileDisplaySerializer(serializers.ModelSerializer):
  answers = MatchProfileAnswersSerializer()
  # answers = serializers.PrimaryKeyRelatedField(queryset=MatchProfileAnswers.objects.all())

  class Meta:
    model = MatchProfileDisplay
    fields = ['user', 'display_name', 'bio', 'city', 'state', 'profile_photo', 'answers']


#########################################################################################################
class FriendsListSerializer(serializers.ModelSerializer):
  class Meta:
    model = FriendsList
    fields = ['user', 'friend']