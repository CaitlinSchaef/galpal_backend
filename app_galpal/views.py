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
  # theres a chance i should just set this to user=user
  answers = MatchProfileAnswers.objects.filter(user=profile)
  answers_serialized = MatchProfileAnswersSerializer(answers, many=True)
  return Response(answers_serialized.data)

# This creates new answers
# this works
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# the parser helps it read data for images
@parser_classes([MultiPartParser, FormParser])
def create_answer(request):
  #  print the data to check 
   print(request.data)
  #  first set an image to be done
   image_answer = None
   if 'image_answer' in request.data:
     image_answer = request.data['image_answer']

   user = request.user
   profile = user.profile
   question_name = request.data['question']
   print("Question Name from Request Data:", question_name) 
   question_data = MatchProfileQuestions.objects.get(question=question_name)
  
   profile_instance = MatchProfileDisplay.objects.get(user=profile)
  
   answer = MatchProfileAnswers.objects.create(
       user = profile,
       question = question_data,
       answer = request.data['answer'],
       image_answer = image_answer, 
       profile_display = profile_instance,
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
  user = request.user
  profile = user.profile
  # may need to change this to user=user
  interest_inventory = InterestInventory.objects.filter(user=profile)
  interest_inventory_serialized = InterestInventorySerializer(interest_inventory, many=True)
  return Response(interest_inventory_serialized.data)

##########################################################################################################
# Match Profile Display

#create new Match Profile Display
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# the parser helps it read data for images
@parser_classes([MultiPartParser, FormParser])
def create_match_profile(request):
   print(request.data)
   profile_photo = None
   if 'profile_photo' in request.data:
     profile_photo = request.data['profile_photo']

   user = request.user
   profile = user.profile
  
   match_display = MatchProfileDisplay.objects.create(
       user = profile,
       display_name = request.data['display_name'],
       bio = request.data['bio'],
       city = request.data['city'],
       state = request.data['state'],
       profile_photo = profile_photo,
   )
   match_display.save()
   match_display_serialized = MatchProfileDisplaySerializer(match_display)
   return Response(match_display_serialized.data)

# get match profile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_match_profile(request):
  user = request.user
  profile = user.profile
  # theres only one match profile display per user, so we can do get 
  
  match_profile = MatchProfileDisplay.objects.get(user=profile)
  match_profile_serialized = MatchProfileDisplaySerializer(match_profile)
  return Response(match_profile_serialized.data)

# update match profile

#########################################################################################################
#requested match stuff

#create a requested match
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# the parser helps it read data for images
@parser_classes([MultiPartParser, FormParser])
def create_match_request(request):
   user = request.user
   profile = user.profile
  
   match_request = RequestedMatch.objects.create(
       requester = profile,
       requested = request.data['requester'],
       status = request.data['status'],
       matched = request.data['matched']
   )
   match_request.save()
   match_request_serialized = RequestedMatchSerializer(match_request)
   return Response(match_request_serialized.data)

#get requested matches
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_match_requests(request):
  match_request = RequestedMatch.objects.all()
  match_request_serialized = RequestedMatchSerializer(match_request, many=True)
  return Response(match_request_serialized.data)

#update match request

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_match_request(request, id):
    try:
        match_request = get_object_or_404(MatchRequest, id=id)

        if match_request.requester != request.user.profile and match_request.requested != request.user.profile:
            return Response({'error': 'Not authorized to update this match request.'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data

        status_updated = data.get('status', match_request.status)
        match_request.status = status_updated

        if status_updated == 'Approved':
            match_request.matched = True

            # Create message channel
            channel_data = {
                'name': f"{match_request.requester.display_name} and {match_request.requested.display_name}",
                'users': [match_request.requester.id, match_request.requested.id]
            }
            channel_serializer = MessageChannelSerializer(data=channel_data)
            if channel_serializer.is_valid():
                channel_serializer.save()
            else:
                return Response(channel_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Add to friends list
            friend_data_1 = {
                'user': match_request.requester.id,
                'friend': match_request.requested.id
            }
            friend_data_2 = {
                'user': match_request.requested.id,
                'friend': match_request.requester.id
            }
            friend_serializer_1 = FriendSerializer(data=friend_data_1)
            friend_serializer_2 = FriendSerializer(data=friend_data_2)
            if friend_serializer_1.is_valid() and friend_serializer_2.is_valid():
                friend_serializer_1.save()
                friend_serializer_2.save()
            else:
                return Response(friend_serializer_1.errors or friend_serializer_2.errors, status=status.HTTP_400_BAD_REQUEST)

        match_request.save()
        return Response(MatchRequestSerializer(match_request).data, status=status.HTTP_200_OK)

    except MatchRequest.DoesNotExist:
        return Response({'error': 'Match request not found.'}, status=status.HTTP_404_NOT_FOUND)

##########################################################################################################
# message channels

#create a message channel
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# the parser helps it read data for images
@parser_classes([MultiPartParser, FormParser])
def create_match_request(request):
   user = request.user
   profile = user.profile
  
   message_channel = RequestedMatch.objects.create(
       name = request.data['name'],
       user = profile
   )
   message_channel.save()
   message_channel_serialized = MessageChannelSerializer(message_channel)
   return Response(message_channel_serialized.data)


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