from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework import viewsets

from .models import *
from .serializers import *

# ‘Get’ = the read
# ‘Post’ = is create
# ‘Put’ = is update
# ‘Delete’ = is delete

#########################################################################################################
# User Views

# Get Profile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
  user = request.user
  profile = user.profile
  serializer = ProfileSerializer(profile, many=False)
  return Response(serializer.data)


#Create New User/User Profile
# This works and saves images, as well as making sure the username, phone number, and email are unique.
@api_view(['POST'])
@permission_classes([])
# the parser helps it read data for images
@parser_classes([MultiPartParser, FormParser])
def create_user(request):
   user = User.objects.create(
       username = request.data['username'],
   )
   user.set_password(request.data['password'])
   user.save()
  

   profile = Profile.objects.create(
       user = user,
       first_name = request.data['first_name'],
       last_name = request.data['last_name'],
       email = request.data['email'],
   )
   profile.save()
   profile_serialized = ProfileSerializer(profile)
   return Response(profile_serialized.data)


#########################################################################################################
# Match Profile Questions

# This gets all of the questions
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_questions(request):
  questions = MatchProfileQuestions.objects.all()
  questions_serialized = MatchProfileQuestionsSerializer(questions, many=True)
  return Response(questions_serialized.data)

#########################################################################################################
# Match Profile Answers

# This gets all of the answers for a specific user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_answers(request):
  user = request.user
  profile = user.profile
  answers = MatchProfileAnswers.objects.filter(user=profile)
  answers_serialized = MatchProfileAnswersSerializer(answers, many=True)
  return Response(answers_serialized.data)

# This creates new answers
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# the parser helps it read data for images
@parser_classes([MultiPartParser, FormParser])
def create_answer(request):
   image_answer = None
   if 'image_answer' in request.data:
     image_answer = request.data['image_answer']

   user = request.user
   profile = profile.user
   question_name = request.data['question']
   question_data = MatchProfileQuestions.objects.get(question=question_name)
  
   answer = MatchProfileAnswers.objects.create(
       user = profile,
       question = question_data,
       answer = request.data['answer'],
       image_answer = image_answer, 
   )
   answer.save()
   answer_serialized = MatchProfileAnswersSerializer(answer)
   return Response(answer_serialized.data)

#########################################################################################################
#interests

#get all interests
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_interests(request):
  interests = Interests.objects.all()
  interests_serialized = InterestsSerializer(interests, many=True)
  return Response(interests_serialized.data)

#########################################################################################################
#interest inventory 

# create new interest inventory 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_interest_inventory(request):
   user = request.user
   print('USER: ', user) 
   profile = user.profile
   print('PROFILE: ', profile)
   
  # Fetch or create Interests instance, this is basically taking the response and translating it into acceptable data 
   interest_name = request.data['interest']
   interest_data = Interests.objects.get(interests=interest_name)

    # Create InterestInventory object
   interest_inventory = InterestInventory.objects.create(
        user=profile,
        interest=interest_data,
    )

   interest_inventory.save()
   interest_serialized = InterestInventorySerializer(interest_inventory)
   return Response(interest_serialized.data)

# get interest inventory 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_interest_inventory(request):
  interest_inventory = InterestInventory.objects.all()
  interest_inventory_serialized = InterestsSerializer(interest_inventory, many=True)
  return Response(interest_inventory_serialized.data)

##########################################################################################################
# message channels



##########################################################################################################
# messages



##########################################################################################################
# Match Profile Display

#create new Match Profile Display
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# the parser helps it read data for images
@parser_classes([MultiPartParser, FormParser])
def create_answer(request):
   profile_photo = None
   if 'profile_photo' in request.data:
     profile_photo = request.data['profile_photo']

   user = request.user
   profile = profile.user
   answer = request.data['answers']
   answer_data = MatchProfileAnswers.objects.all()
  
   match_display = MatchProfileAnswers.objects.create(
       user = profile,
       display_name = request.data['display_name'],
       bio = request.data['bio'],
       city = request.data['city'],
       state = request.data['state'],
       profile_photo = profile_photo,
       answers = answer_data,
   )
   match_display.save()
   match_display_serialized = MatchProfileDisplaySerializer(match_display)
   return Response(match_display_serialized.data)

##########################################################################################################
# class views for back end

class InterestsViewSet(viewsets.ModelViewSet):
  queryset = Interests.objects.all()
  serializer_class = InterestsSerializer

class MatchProfileQuestionsViewSet(viewsets.ModelViewSet):
  queryset = MatchProfileQuestions.objects.all()
  serializer_class = MatchProfileQuestionsSerializer