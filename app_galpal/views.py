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

# Create New User
#Create New User/User Profile
@api_view(['POST'])
@permission_classes([])
# the parser helps it read data
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
   profile_serialized = ProfileSerializer(profile)
   if profile_serialized.is_valid():
    profile.save()
    return Response(profile_serialized.data, status=status.HTTP_201_CREATED)
   return Response(profile_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


#########################################################################################################
# Match Profile Answers

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @parser_classes([MultiPartParser, FormParser])
# def get_images(request):
#   images = Image.objects.all()
#   # default is many=False, which would just serialize one object, this will return a whole list
#   images_serialized = ImageSerializer(images, many=True)
#   return Response(images_serialized.data)

##########################################################################################################
# class views for back end

class InterestsViewSet(viewsets.ModelViewSet):
  queryset = Interests.objects.all()
  serializer_class = InterestsSerializer

class MatchProfileQuestionsViewSet(viewsets.ModelViewSet):
  queryset = MatchProfileQuestions.objects.all()
  serializer_class = MatchProfileQuestionsSerializer