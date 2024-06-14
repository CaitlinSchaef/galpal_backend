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
  
   profile_photo = None
   if 'profile_photo' in request.data:
     profile_photo = request.data['profile_photo']

   profile = Profile.objects.create(
       user = user,
       first_name = request.data['first_name'],
       last_name = request.data['last_name'],
       display_name = request.data['display_name'],
       bio = request.data['bio'],
       email = request.data['email'],
       phone = request.data['phone'],
       city = request.data['city'],
       state = request.data['state'],
       profile_photo = profile_photo
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
  answers = MatchProfileAnswers.objects.filter(user=request.data['user'])
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
  #  I might need to use this, but also since it's serialized I feel like I could just use it?
  #  question_pk = MatchProfileQuestions.objects.filter(question=request.data['question']).first().pk
   answer = MatchProfileAnswers.objects.create(
       user = user,
       question = request.data['question'],
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
   
  # Fetch or create Interests instance
   interest_name = request.data['interest']
   interest_instance = Interests.objects.get(interests=interest_name)

    # Create InterestInventory object
   interest_inventory = InterestInventory.objects.create(
        user=profile,
        interest=interest_instance,
    )

   interest_inventory.save()
   interest_serialized = InterestInventorySerializer(interest_inventory)
   return Response(interest_serialized.data)

# get interest inventory 


##########################################################################################################
# message channels



##########################################################################################################
# messages



##########################################################################################################
# class views for back end

class InterestsViewSet(viewsets.ModelViewSet):
  queryset = Interests.objects.all()
  serializer_class = InterestsSerializer

class MatchProfileQuestionsViewSet(viewsets.ModelViewSet):
  queryset = MatchProfileQuestions.objects.all()
  serializer_class = MatchProfileQuestionsSerializer