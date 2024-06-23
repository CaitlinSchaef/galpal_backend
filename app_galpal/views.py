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

#delete user, not sure if this works
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
   user = request.user
   user_to_delete = User.objects.get(user=user)
   user_to_delete.delete()
   return Response(status=status.HTTP_202_ACCEPTED)

# not sure if I need this, doesn't have url
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get__all_profiles(request):
  serializer = ProfileSerializer()
  return Response(serializer.data)



# Get Profile, is is just getting the current users profile, it works
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
  user = request.user
  profile = user.profile
  serializer = ProfileSerializer(profile, many=False)
  return Response(serializer.data)



#Create New User/User Profile
# This works and makes sure the username, phone number, and email are unique.
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

# This gets all of the questions, this works
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_questions(request):
  questions = MatchProfileQuestions.objects.all()
  questions_serialized = MatchProfileQuestionsSerializer(questions, many=True)
  return Response(questions_serialized.data)

#########################################################################################################
# Match Profile Answers

# This gets all of the answers for a specific user, this works
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_answers(request):
  user = request.user
  profile = user.profile
  # theres a chance i should just set this to user=user
  answers = MatchProfileAnswers.objects.filter(user=profile)
  answers_serialized = MatchProfileAnswersSerializer(answers, many=True)
  return Response(answers_serialized.data)

# get all user answers, this works 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_profile_answers(request):
  answers = MatchProfileAnswers.objects.all()
  answers_serialized = MatchProfileAnswersSerializer(answers, many=True)
  return Response(answers_serialized.data)

# This creates new answers, this works
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

# Update MatchProfileAnswers, NOT SURE IF WORKS
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_answer(request, pk):
    try:
        match_profile_answer = MatchProfileAnswers.objects.get(pk=pk)
    except MatchProfileAnswers.DoesNotExist:
        return Response({'error': 'MatchProfileAnswers not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = MatchProfileAnswersSerializer(match_profile_answer, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#########################################################################################################
#interests

#get all interests, this works
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_interests(request):
  interests = Interests.objects.all()
  interests_serialized = InterestsSerializer(interests, many=True)
  return Response(interests_serialized.data)

#########################################################################################################
#interest inventory 

# create new interest inventory, this works
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

# get interest inventory of current user, this works
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_interest_inventory(request):
  user = request.user
  profile = user.profile
  # may need to change this to user=user
  interest_inventory = InterestInventory.objects.filter(user=profile)
  interest_inventory_serialized = InterestInventorySerializer(interest_inventory, many=True)
  return Response(interest_inventory_serialized.data)

# get all interest inventories, not sure if works
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_interest_inventories(request):
  interest_inventory = InterestInventory.objects.all()
  interest_inventory_serialized = InterestInventorySerializer(interest_inventory, many=True)
  return Response(interest_inventory_serialized.data)

# update interest inventory, this works, had to make it a put instead of patch because of multiple instances 
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_interest_inventory(request):
    user = request.user
    profile = user.profile

    # Remove the existing interests for the user
    InterestInventory.objects.filter(user=profile).delete()

    # Create new interests for the user
    interests_data = request.data.get('interests', [])
    new_interests = []
    for interest_name in interests_data:
        interest = Interests.objects.get(interests=interest_name)
        new_interests.append(InterestInventory(user=profile, interest=interest))
    
    InterestInventory.objects.bulk_create(new_interests)

    # Fetch the updated interests
    updated_interests = InterestInventory.objects.filter(user=profile)
    serializer = InterestInventorySerializer(updated_interests, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


##########################################################################################################
# Match Profile Display

#create new Match Profile Display, this works
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

# get match profile, this works
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_match_profile(request):
  user = request.user
  profile = user.profile
  # theres only one match profile display per user, so we can do get 
  
  match_profile = MatchProfileDisplay.objects.get(user=profile)
  match_profile_serialized = MatchProfileDisplaySerializer(match_profile)
  return Response(match_profile_serialized.data)

# get all match profiles, this works 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_match_profiles(request):
  profiles = MatchProfileDisplay.objects.all()
  profiles_serialized = MatchProfileDisplaySerializer(profiles, many=True)
  return Response(profiles_serialized.data)

# Update match profile, works now yaya
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_match_profile(request):
    user = request.user
    profile = user.profile
    print('REQUEST DATA:', request.data)
    try:
        match_profile = MatchProfileDisplay.objects.get(user=profile)
    except MatchProfileDisplay.DoesNotExist:
        return Response({'error': 'MatchProfileDisplay not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Remove 'profile_photo' from the request data if it's not a file
    data = request.data.copy()
    if 'profile_photo' in data and isinstance(data['profile_photo'], str):
        del data['profile_photo']

    serializer = MatchProfileDisplaySerializer(match_profile, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#########################################################################################################
#requested match stuff

#create a requested match, this works for passing and friending 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_match_request(request):
   user = request.user
   profile = user.profile

  # this produces a string of the user id 
   requested_display_name = request.data['requested']
    # this prints a Display name 
   print('DATA FROM REQUESTED: ', requested_display_name)
  #  first get the match profile, then get the profile instance from that 
   match_profile_display = MatchProfileDisplay.objects.get(display_name=requested_display_name)
   profile_instance = match_profile_display.user
  
   match_request = RequestedMatch.objects.create(
       requester = profile,
       requested = profile_instance,
       status = request.data['status']
   )
   match_request.save()
   match_request_serialized = RequestedMatchSerializer(match_request)
   return Response(match_request_serialized.data)

#get requested matches, this works 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_match_requests(request):
  user = request.user
  profile = user.profile
  try:
      match_requests = RequestedMatch.objects.filter(requester=profile) | RequestedMatch.objects.filter(requested=profile)
      match_request_serialized = RequestedMatchSerializer(match_requests, many=True)
      return Response(match_request_serialized.data)
  except RequestedMatch.DoesNotExist:
      print('HEY! this is fine, they just dont have any matches yet')
      return Response(status=status.HTTP_200_OK)


#update match request
# using a patch because we will really only update status or matched 
# Update match request, this works 
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_match_request(request, id):
    user = request.user
    profile = user.profile

    try:
        # serialized the requested match id so that we could use that in the front end
        match_request = RequestedMatch.objects.get(id=id)

        # checks if the current user is either the requester or the requested user
        if match_request.requester != profile and match_request.requested != profile:
            return Response({'error': 'Not authorized to update this match request.'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data

        status_updated = data.get('status', match_request.status)
        match_request.status = status_updated

        if status_updated == 'Approved':
            match_request.matched = True

            # Create message channel
            channel_data = {
                'name': f"{match_request.requester.user.username} and {match_request.requested.user.username}",
                'user1': [match_request.requester.id],
                'user2': [match_request.requested.id],
            }
            channel_serializer = MessageChannelSerializer(data=channel_data)
            if channel_serializer.is_valid():
                channel_serializer.save()
            else:
                return Response(channel_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Add to friends list, assigning both as user and friend to update both lists
            friend_data_1 = {
                'user': match_request.requester.id,
                'friend': [match_request.requested.id]
            }
            friend_data_2 = {
                'user': match_request.requested.id,
                'friend': [match_request.requester.id]
            }
            friend_serializer_1 = FriendsListSerializer(data=friend_data_1)
            friend_serializer_2 = FriendsListSerializer(data=friend_data_2)
            if friend_serializer_1.is_valid() and friend_serializer_2.is_valid():
                friend_serializer_1.save()
                friend_serializer_2.save()
            else:
                return Response(friend_serializer_1.errors or friend_serializer_2.errors, status=status.HTTP_400_BAD_REQUEST)

        match_request.save()
        return Response(RequestedMatchSerializer(match_request).data, status=status.HTTP_200_OK)

    except RequestedMatch.DoesNotExist:
        return Response({'error': 'Match request not found.'}, status=status.HTTP_404_NOT_FOUND)
    
##########################################################################################################
# message channels

#get message channel, this works
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_message_channel(request):
  user = request.user
  profile = user.profile
  # I need to get all of the message channels where the profile = user1 or user 2, will this work?
  # if you get an error with getting message channels check here 
  message_channel = MessageChannel.objects.filter(user1=profile) | MessageChannel.objects.filter(user2=profile)
  message_channel_serialized = MessageChannelSerializer(message_channel, many=True)
  return Response(message_channel_serialized.data)


#create a message channel, do not think I'll use this
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_message_channel(request):
   user = request.user
   profile = user.profile
  
   message_channel = MessageChannel.objects.create(
       name = request.data['name'],
       user1 = profile,
       user2 = request.data['user2']
   )
   message_channel.save()
   message_channel_serialized = MessageChannelSerializer(message_channel)
   return Response(message_channel_serialized.data)


##########################################################################################################
# messages

#create a new message, this works
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_message(request):
   user = request.user
   profile = user.profile
   try:
      message_channel = MessageChannel.objects.get(name=request.data['message_channel'])
   except MessageChannel.DoesNotExist:
        return Response({'error': 'MessageChannel not found'}, status=status.HTTP_404_NOT_FOUND)

   message = Message.objects.create(
        message_channel=message_channel,
        message_author=profile,
        message_content=request.data['message_content'],
    )
   message.save()
   message_serialized = MessageSerializer(message)
   return Response(message_serialized.data)

#get messages
# need to get messages for specific message channels, not authors, this works 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request):
  message_channel_name = request.query_params.get('message_channel')
  if not message_channel_name:
      return Response({'error': 'message_channel is required'}, status=status.HTTP_400_BAD_REQUEST)

  try:
      message_channel = MessageChannel.objects.get(name=message_channel_name)
  except MessageChannel.DoesNotExist:
      return Response({'error': 'MessageChannel not found'}, status=status.HTTP_404_NOT_FOUND)

  messages = Message.objects.filter(message_channel=message_channel)
  message_serialized = MessageSerializer(messages, many=True)
  return Response(message_serialized.data)

##########################################################################################################
# friends list
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friends_list(request):
  user = request.user
  profile = user.profile
  friend_list = FriendsList.objects.filter(user=profile)
  friend_list_serialized = FriendsListSerializer(friend_list, many=True)
  return Response(friend_list_serialized.data)


##########################################################################################################
# class views for back end

class InterestsViewSet(viewsets.ModelViewSet):
  queryset = Interests.objects.all()
  serializer_class = InterestsSerializer

class MatchProfileQuestionsViewSet(viewsets.ModelViewSet):
  queryset = MatchProfileQuestions.objects.all()
  serializer_class = MatchProfileQuestionsSerializer